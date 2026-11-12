# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.1 -> 14.0.1.2.0
#
# Changes: fills the four new Many2many relations (dominant and
#          secondary character tags, dominant and secondary character
#          indicators) of the learning artifact from the legacy
#          columns and table renamed by the pre script. The legacy
#          data is read with SQL, since the old fields are no longer
#          in the registry.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

ARTIFACT_TABLE = "school_learning_artifact"
OLD_INDICATOR_TABLE = "school_learning_artifact_character_indicator_rel"
DOMINANT_TAG_REL = "school_learning_artifact_dominant_subconstruct_rel"
SECONDARY_TAG_REL = "school_learning_artifact_secondary_subconstruct_rel"
DOMINANT_INDICATOR_REL = "school_learning_artifact_dominant_indicator_rel"
SECONDARY_INDICATOR_REL = "school_learning_artifact_secondary_indicator_rel"


def _insert_tags(cr, relation, source_query):
    """Insert artifact and tag pairs that are not in the relation yet.

    :param cr: the database cursor
    :param relation: name of the Many2many table of the tags
    :param source_query: query that returns (artifact_id, subconstruct_id)
    :return: number of inserted rows
    """
    return openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(rel)s (artifact_id, subconstruct_id)
        SELECT DISTINCT src.artifact_id, src.subconstruct_id
        FROM (%(source)s) AS src
        WHERE NOT EXISTS (
            SELECT 1 FROM %(rel)s rel
            WHERE rel.artifact_id = src.artifact_id
            AND rel.subconstruct_id = src.subconstruct_id
        )
        """
        % {"rel": relation, "source": source_query},
    )


def _insert_indicators(cr, relation, source_query):
    """Insert artifact and indicator pairs that are not in the relation.

    :param cr: the database cursor
    :param relation: name of the Many2many table of the indicators
    :param source_query: query that returns (artifact_id, indicator_id)
    :return: number of inserted rows
    """
    return openupgrade.logged_query(
        cr,
        """
        INSERT INTO %(rel)s (artifact_id, indicator_id)
        SELECT DISTINCT src.artifact_id, src.indicator_id
        FROM (%(source)s) AS src
        WHERE NOT EXISTS (
            SELECT 1 FROM %(rel)s rel
            WHERE rel.artifact_id = src.artifact_id
            AND rel.indicator_id = src.indicator_id
        )
        """
        % {"rel": relation, "source": source_query},
    )


@openupgrade.migrate()
def migrate(env, version):
    """Move the legacy character tags and indicators to the new fields.

    The legacy columns and table are read only when they exist. A
    secondary tag equal to the dominant tag is kept as dominant only.
    An indicator of the dominant tag becomes a dominant indicator and
    an indicator of the other secondary tag becomes a secondary one.
    An artifact with indicators and without any old tag gets the
    sub-construct of each indicator as a dominant tag and the
    indicators as dominant indicators. An indicator without a
    sub-construct cannot be placed and is left out.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; inserts rows in the four new relations
    """
    cr = env.cr
    primary = openupgrade.get_legacy_name("primary_subconstruct_id")
    secondary = openupgrade.get_legacy_name("secondary_subconstruct_id")
    legacy_table = openupgrade.get_legacy_name(OLD_INDICATOR_TABLE)
    has_primary = openupgrade.column_exists(cr, ARTIFACT_TABLE, primary)
    has_secondary = openupgrade.column_exists(cr, ARTIFACT_TABLE, secondary)
    has_indicator = openupgrade.table_exists(cr, legacy_table)
    if has_primary:
        rows = _insert_tags(
            cr,
            DOMINANT_TAG_REL,
            'SELECT id AS artifact_id, "%s" AS subconstruct_id '
            'FROM %s WHERE "%s" IS NOT NULL' % (primary, ARTIFACT_TABLE, primary),
        )
        _logger.info("Dominant tags from the old dominant tag: %s row(s).", rows)
    if has_secondary:
        other = (
            ' AND ("%s" IS NULL OR "%s" <> "%s")' % (primary, secondary, primary)
            if has_primary
            else ""
        )
        rows = _insert_tags(
            cr,
            SECONDARY_TAG_REL,
            'SELECT id AS artifact_id, "%s" AS subconstruct_id '
            'FROM %s WHERE "%s" IS NOT NULL%s'
            % (secondary, ARTIFACT_TABLE, secondary, other),
        )
        _logger.info("Secondary tags from the old secondary tag: %s row(s).", rows)
    if has_indicator and has_primary:
        rows = _insert_indicators(
            cr,
            DOMINANT_INDICATOR_REL,
            "SELECT rel.artifact_id AS artifact_id, "
            "rel.indicator_id AS indicator_id "
            "FROM %s rel "
            "JOIN school_character_indicator ind ON ind.id = rel.indicator_id "
            'JOIN %s art ON art.id = rel.artifact_id AND art."%s" = '
            "ind.subconstruct_id" % (legacy_table, ARTIFACT_TABLE, primary),
        )
        _logger.info("Dominant indicators of the old dominant tag: %s.", rows)
    if has_indicator and has_secondary:
        other = (
            ' AND (art."%s" IS NULL OR art."%s" <> art."%s")'
            % (primary, secondary, primary)
            if has_primary
            else ""
        )
        rows = _insert_indicators(
            cr,
            SECONDARY_INDICATOR_REL,
            "SELECT rel.artifact_id AS artifact_id, "
            "rel.indicator_id AS indicator_id "
            "FROM %s rel "
            "JOIN school_character_indicator ind ON ind.id = rel.indicator_id "
            'JOIN %s art ON art.id = rel.artifact_id AND art."%s" = '
            "ind.subconstruct_id%s" % (legacy_table, ARTIFACT_TABLE, secondary, other),
        )
        _logger.info("Secondary indicators of the old secondary tag: %s.", rows)
    if has_indicator:
        untagged = ""
        if has_primary:
            untagged += ' AND art."%s" IS NULL' % primary
        if has_secondary:
            untagged += ' AND art."%s" IS NULL' % secondary
        base = (
            "FROM %s rel "
            "JOIN school_character_indicator ind ON ind.id = rel.indicator_id "
            "JOIN %s art ON art.id = rel.artifact_id "
            "WHERE ind.subconstruct_id IS NOT NULL%s"
            % (legacy_table, ARTIFACT_TABLE, untagged)
        )
        rows = _insert_tags(
            cr,
            DOMINANT_TAG_REL,
            "SELECT rel.artifact_id AS artifact_id, "
            "ind.subconstruct_id AS subconstruct_id " + base,
        )
        _logger.info("Dominant tags of indicators without a tag: %s row(s).", rows)
        rows = _insert_indicators(
            cr,
            DOMINANT_INDICATOR_REL,
            "SELECT rel.artifact_id AS artifact_id, "
            "rel.indicator_id AS indicator_id " + base,
        )
        _logger.info("Dominant indicators without a tag: %s row(s).", rows)
