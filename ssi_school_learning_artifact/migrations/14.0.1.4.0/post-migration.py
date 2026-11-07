# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.3.0 -> 14.0.1.4.0
#
# Changes: curation moved from a free score typed per aspect and a
#          single ethics result on the artifact to a level picked per
#          aspect and ethics gate aspects. Odoo creates the new
#          columns and tables by itself but cannot invent the data
#          that fills them, so this script converts the existing
#          data: it builds one level per score of every aspect, links
#          the scored rows to their level, gives every rubric one
#          ethics gate aspect with the levels Pass and Fail, turns the
#          old ethics result (and its reason and assessor) of every
#          artifact into an answered gate row, recomputes the stored
#          fields derived from them without touching the totals, and
#          finally removes the ethics reason master and the columns
#          that no field uses any more.
#
# This is a "post" script (not "pre") because the new tables and
# columns must already exist, while the old columns it reads
# (min_score, max_score, ethics_result, ethics_reason_id,
# ethics_assessor_id) are still in the database: Odoo never drops a
# column by itself.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

T_ARTIFACT = "school_learning_artifact"
T_RUBRIC = "school_learning_artifact_rubric"
T_CRITERION = "school_learning_artifact_rubric_criterion"
T_LEVEL = "school_learning_artifact_rubric_criterion_level"
T_SCORE = "school_learning_artifact_score"
T_REASON = "school_learning_artifact_ethics_reason"
T_REASON_SCHOOL_REL = "school_la_ethics_reason_school_rel"
T_ETHICS_GROUP_REL = "school_la_rubric_ethics_group_rel"
T_CRITERION_GROUP_REL = "school_la_criterion_group_rel"

REASON_XML_IDS = [
    # Dependents first: menu, action, views, access rows, group.
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_menu",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_action",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_view_search",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_view_form",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_all_access",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_user_access",
    "ssi_school_learning_artifact.school_learning_artifact_ethics_reason_group",
]

NOW = "(now() AT TIME ZONE 'UTC')"


def _create_levels(cr):
    """Create one level per score of every scored aspect.

    The level range comes from the old ``min_score``/``max_score`` of
    the aspect and the text of a level is ``Score N``. Aspects that
    already own a level for a score are left alone.

    :param cr: the database cursor
    :return: nothing; inserts level rows
    """
    rows = openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(level)s
            (criterion_id, sequence, score, name, is_fail,
             create_uid, create_date, write_uid, write_date)
        SELECT c.id, g.n, g.n, 'Score ' || g.n, FALSE,
               1, %(now)s, 1, %(now)s
        FROM %(criterion)s c
        CROSS JOIN LATERAL generate_series(c.min_score, c.max_score) AS g(n)
        WHERE c.aspect_type = 'score'
          AND NOT EXISTS (
              SELECT 1 FROM %(level)s l
              WHERE l.criterion_id = c.id AND l.score = g.n
          )
        """
        % {"level": T_LEVEL, "criterion": T_CRITERION, "now": NOW},
    )
    _logger.info("Created %s level(s) from the old score ranges.", rows)


def _link_scores_to_levels(cr):
    """Link every scored row to the level of its score.

    A score of zero means "not assessed yet" and keeps the row empty.
    ``assessor_id`` and ``date_score`` are not touched.

    :param cr: the database cursor
    :return: nothing; updates score rows
    """
    rows = openupgrade.logged_query(
        cr,
        """
        UPDATE %(score)s s
        SET aspect_type = c.aspect_type
        FROM %(criterion)s c
        WHERE c.id = s.criterion_id AND s.aspect_type IS NULL
        """
        % {"score": T_SCORE, "criterion": T_CRITERION},
    )
    _logger.info("Stamped aspect_type on %s score row(s).", rows)
    rows = openupgrade.logged_query(
        cr,
        """
        UPDATE %(score)s s
        SET level_id = m.level_id, level_text = m.name
        FROM (
            SELECT DISTINCT ON (l.criterion_id, l.score)
                   l.id AS level_id, l.criterion_id, l.score, l.name
            FROM %(level)s l
            ORDER BY l.criterion_id, l.score, l.id
        ) m
        WHERE m.criterion_id = s.criterion_id
          AND m.score = s.score
          AND s.score > 0
          AND s.level_id IS NULL
        """
        % {"score": T_SCORE, "level": T_LEVEL},
    )
    _logger.info("Linked %s score row(s) to their level.", rows)
    cr.execute(
        "SELECT count(*) FROM school_learning_artifact_score "
        "WHERE score > 0 AND level_id IS NULL"
    )
    left = cr.fetchone()[0]
    if left:
        _logger.warning("%s scored row(s) match no level of their aspect.", left)


def _create_gate_aspects(cr):
    """Give every rubric without a gate aspect one ethics gate aspect.

    The aspect has code ``EG``, the secondary assessor slot, the
    levels Pass and Fail, and takes over the old ethics assessor
    groups of the rubric.

    :param cr: the database cursor
    :return: nothing; inserts aspect, level and group rows
    """
    rows = openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(criterion)s
            (rubric_id, sequence, code, name, aspect_type, min_score,
             max_score, knockout_score, assessor_slot,
             create_uid, create_date, write_uid, write_date)
        SELECT r.id,
               COALESCE((SELECT max(c.sequence) FROM %(criterion)s c
                         WHERE c.rubric_id = r.id), 0) + 10,
               'EG', 'Ethics Gate', 'gate', 0, 0, 0, 'secondary',
               1, %(now)s, 1, %(now)s
        FROM %(rubric)s r
        WHERE NOT EXISTS (
            SELECT 1 FROM %(criterion)s c
            WHERE c.rubric_id = r.id AND c.aspect_type = 'gate'
        )
        """
        % {"criterion": T_CRITERION, "rubric": T_RUBRIC, "now": NOW},
    )
    _logger.info("Created %s ethics gate aspect(s).", rows)
    rows = openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(level)s
            (criterion_id, sequence, score, name, is_fail,
             create_uid, create_date, write_uid, write_date)
        SELECT c.id, v.seq, 0, v.name, v.is_fail,
               1, %(now)s, 1, %(now)s
        FROM %(criterion)s c
        CROSS JOIN (
            VALUES (10, 'Pass', FALSE), (20, 'Fail', TRUE)
        ) AS v(seq, name, is_fail)
        WHERE c.aspect_type = 'gate'
          AND NOT EXISTS (
              SELECT 1 FROM %(level)s l WHERE l.criterion_id = c.id
          )
        """
        % {"level": T_LEVEL, "criterion": T_CRITERION, "now": NOW},
    )
    _logger.info("Created %s Pass/Fail level(s) for gate aspect(s).", rows)
    if openupgrade.table_exists(cr, T_ETHICS_GROUP_REL):
        rows = openupgrade.logged_query(
            cr,
            """
            INSERT INTO %(crel)s (criterion_id, group_id)
            SELECT c.id, e.group_id
            FROM %(criterion)s c
            JOIN %(erel)s e ON e.rubric_id = c.rubric_id
            WHERE c.aspect_type = 'gate' AND c.code = 'EG'
              AND NOT EXISTS (
                  SELECT 1 FROM %(crel)s x
                  WHERE x.criterion_id = c.id AND x.group_id = e.group_id
              )
            """
            % {
                "crel": T_CRITERION_GROUP_REL,
                "criterion": T_CRITERION,
                "erel": T_ETHICS_GROUP_REL,
            },
        )
        _logger.info("Copied %s ethics assessor group(s) to gate aspects.", rows)


def _create_gate_rows(cr):
    """Turn the old ethics result of every artifact into a gate row.

    Every artifact that has score rows or an ethics result gets one
    row for the ethics gate aspect of its rubric. The level follows
    the old result (``pass`` or ``fail``), the assessor is the old
    ethics assessor, and a failed result with a reason gets the level
    text ``Fail: <reason name>``. Without an old result the row stays
    empty. Artifacts without a rubric are skipped.

    :param cr: the database cursor
    :return: nothing; inserts score rows
    """
    has_assessor = openupgrade.column_exists(cr, T_ARTIFACT, "ethics_assessor_id")
    has_reason = openupgrade.column_exists(
        cr, T_ARTIFACT, "ethics_reason_id"
    ) and openupgrade.table_exists(cr, T_REASON)
    assessor = "a.ethics_assessor_id" if has_assessor else "NULL"
    reason_join = (
        "LEFT JOIN %s r ON r.id = a.ethics_reason_id" % T_REASON if has_reason else ""
    )
    reason_name = "r.name" if has_reason else "NULL"
    rows = openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(score)s
            (artifact_id, criterion_id, sequence, aspect_type, level_id,
             level_text, score, assessor_id,
             create_uid, create_date, write_uid, write_date)
        SELECT a.id, g.id, g.sequence, 'gate', lv.id,
               CASE
                   WHEN lv.id IS NULL THEN NULL
                   WHEN a.ethics_result = 'fail' AND %(reason_name)s IS NOT NULL
                       THEN 'Fail: ' || %(reason_name)s
                   ELSE lv.name
               END,
               0, CASE WHEN lv.id IS NULL THEN NULL ELSE %(assessor)s END,
               1, %(now)s, 1, %(now)s
        FROM %(artifact)s a
        JOIN LATERAL (
            SELECT c.id, c.sequence FROM %(criterion)s c
            WHERE c.rubric_id = a.rubric_id AND c.aspect_type = 'gate'
            ORDER BY c.sequence, c.id LIMIT 1
        ) g ON TRUE
        LEFT JOIN LATERAL (
            SELECT l.id, l.name FROM %(level)s l
            WHERE l.criterion_id = g.id
              AND l.is_fail = (a.ethics_result = 'fail')
            ORDER BY l.sequence, l.id LIMIT 1
        ) lv ON a.ethics_result IS NOT NULL
        %(reason_join)s
        WHERE a.rubric_id IS NOT NULL
          AND (
              a.ethics_result IS NOT NULL
              OR EXISTS (
                  SELECT 1 FROM %(score)s s WHERE s.artifact_id = a.id
              )
          )
          AND NOT EXISTS (
              SELECT 1 FROM %(score)s s
              JOIN %(criterion)s c ON c.id = s.criterion_id
              WHERE s.artifact_id = a.id AND c.aspect_type = 'gate'
          )
        """
        % {
            "score": T_SCORE,
            "artifact": T_ARTIFACT,
            "criterion": T_CRITERION,
            "level": T_LEVEL,
            "assessor": assessor,
            "reason_join": reason_join,
            "reason_name": reason_name,
            "now": NOW,
        },
    )
    _logger.info("Created %s ethics gate row(s) on artifacts.", rows)
    cr.execute(
        "SELECT count(*) FROM school_learning_artifact "
        "WHERE rubric_id IS NULL AND ethics_result IS NOT NULL"
    )
    skipped = cr.fetchone()[0]
    if skipped:
        _logger.warning("%s artifact(s) without rubric keep no gate row.", skipped)


def _recompute(env):
    """Recompute the stored fields that derive from the gate rows.

    The ethics result, the total score and the curation status are
    rebuilt with ``add_to_compute`` and ``flush``: the model
    ``write()`` is not called, so no guard of the artifact fires.

    :param env: the migration environment
    :return: nothing; recomputes stored fields
    """
    artifacts = env[T_ARTIFACT].with_context(active_test=False).search([])
    field_names = ["ethics_result", "total_score", "curation_status_id"]
    for field_name in field_names:
        env.add_to_compute(artifacts._fields[field_name], artifacts)
    artifacts.flush(field_names)
    _logger.info(
        "Recomputed %s on %s artifact(s).", ", ".join(field_names), len(artifacts)
    )


def _purge_ethics_reason(env):
    """Remove the ethics reason master and the unused old columns.

    The order is binding: the columns that point to the reason table
    go first, then the many2many relation tables, then the table of
    the reason itself, because dropping a referenced table before its
    dependents raises ``DependentObjectsStillExist`` and rolls the
    whole upgrade back.

    :param env: the migration environment
    :return: nothing; drops columns, tables and orphan metadata
    """
    cr = env.cr
    old_columns = [
        (T_ARTIFACT, column)
        for column in ("ethics_reason_id", "ethics_assessor_id")
        if openupgrade.column_exists(cr, T_ARTIFACT, column)
    ]
    if old_columns:
        openupgrade.drop_columns(cr, old_columns)
    openupgrade.logged_query(cr, "DROP TABLE IF EXISTS %s" % T_ETHICS_GROUP_REL)
    openupgrade.logged_query(cr, "DROP TABLE IF EXISTS %s" % T_REASON_SCHOOL_REL)
    openupgrade.logged_query(cr, "DROP TABLE IF EXISTS %s" % T_REASON)
    rows = openupgrade.logged_query(
        cr,
        "DELETE FROM ir_model_relation WHERE name IN %s",
        ((T_ETHICS_GROUP_REL, T_REASON_SCHOOL_REL),),
    )
    _logger.info("Deleted %s ir.model.relation row(s).", rows)
    rows = openupgrade.logged_query(
        cr,
        "DELETE FROM ir_translation WHERE name LIKE %s",
        (T_REASON + ",%",),
    )
    _logger.info("Deleted %s ir.translation row(s).", rows)
    existing = [
        xml_id for xml_id in REASON_XML_IDS if env.ref(xml_id, raise_if_not_found=False)
    ]
    if existing:
        openupgrade.delete_records_safely_by_xml_id(env, existing)


@openupgrade.migrate()
def migrate(env, version):
    """Convert the curation data to levels and ethics gate rows.

    Builds the levels, links the scored rows, creates the ethics gate
    aspects and rows, recomputes the derived stored fields and purges
    the ethics reason master. Every step is guarded by
    ``column_exists``/``table_exists`` or by ``NOT EXISTS``, so a
    second run changes nothing.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; converts the curation data in place
    """
    cr = env.cr
    if not openupgrade.table_exists(cr, T_LEVEL):
        _logger.warning("Table %s is missing: nothing to convert.", T_LEVEL)
        return
    if openupgrade.column_exists(cr, T_CRITERION, "min_score"):
        _create_levels(cr)
    _link_scores_to_levels(cr)
    _create_gate_aspects(cr)
    if openupgrade.column_exists(cr, T_ARTIFACT, "ethics_result"):
        _create_gate_rows(cr)
    _recompute(env)
    _purge_ethics_reason(env)
