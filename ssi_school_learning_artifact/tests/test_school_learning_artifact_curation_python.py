# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.modules.module import get_module_path
from odoo.tests import tagged
from odoo.tools import mute_logger

MODULE = "ssi_school_learning_artifact"
MIGRATION_PATH = os.path.join(
    "migrations",
    "14.0.1.4.0",
    "post-migration.py",
)
LEVEL_MODEL = "school_learning_artifact_rubric_criterion_level"
SNAPSHOT_SQL = """
    SELECT id, state, total_score, curation_status_id, ethics_result
    FROM school_learning_artifact
    WHERE id IN %s
    ORDER BY id
"""


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactCurationPython(YamlTransactionCase):
    """Test the curation rules that YAML scenarios cannot express.

    Covers the restricted deletion of a level that an answer uses and
    the conversion script of the 14.0.1.4.0 upgrade.
    """

    def setUp(self):
        """Create the school, the rubric and the statuses of the tests.

        :return: None
        """
        super().setUp()
        env = self.env
        grade_type = env["school_grade_type"].create(
            {"name": "PY Grade Type", "code": "/", "sequence": 10}
        )
        branch = env["school_branch"].create({"name": "PY Branch", "code": "/"})
        self.school = env["school"].create(
            {
                "name": "PY School",
                "code": "/",
                "grade_type_id": grade_type.id,
                "branch_id": branch.id,
            }
        )
        grade = env["school_grade"].create(
            {
                "name": "PY Grade",
                "code": "/",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        self.grade_class = env["school_grade_class"].create(
            {
                "name": "PY Class",
                "code": "/",
                "school_id": self.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        self.year = env["school_academic_year"].create(
            {
                "name": "PY Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        contact = env["res.partner"].create({"name": "PY Student Contact"})
        self.student = env["school_student"].create(
            {
                "name": "PY Student",
                "code": "/",
                "contact_id": contact.id,
                "school_id": self.school.id,
            }
        )
        self.area = env["school_learning_artifact_area"].create(
            {
                "name": "PY Area",
                "code": "/",
                "school_id": self.school.id,
                "area_type": "subject",
            }
        )
        self.category = env["school_learning_artifact_category"].create(
            {"name": "PY Category", "code": "/"}
        )
        obj_status = env["school_learning_artifact_curation_status"]
        self.eligible = obj_status.create(
            {
                "name": "PY Eligible",
                "code": "/",
                "category": "eligible",
                "school_ids": [(6, 0, self.school.ids)],
            }
        )
        self.revision = obj_status.create(
            {
                "name": "PY Revision",
                "code": "/",
                "category": "revision",
                "school_ids": [(6, 0, self.school.ids)],
            }
        )
        self.rejected = obj_status.create(
            {
                "name": "PY Rejected",
                "code": "/",
                "category": "rejected",
                "school_ids": [(6, 0, self.school.ids)],
            }
        )

    def _create_rubric(self, with_levels):
        """Create the rubric of the school with two scored aspects.

        :param with_levels: when True the aspects get levels one to
            three, otherwise they get none (the shape that the
            upgrade starts from)
        :return: the ``school_learning_artifact_rubric`` record
        """
        levels = []
        if with_levels:
            levels = [
                (0, 0, {"sequence": n * 10, "score": n, "name": "PY Level %s" % n})
                for n in (1, 2, 3)
            ]
        return self.env["school_learning_artifact_rubric"].create(
            {
                "name": "PY Rubric",
                "code": "/",
                "school_ids": [(6, 0, self.school.ids)],
                "ethics_fail_status_id": self.rejected.id,
                "criterion_ids": [
                    (
                        0,
                        0,
                        {
                            "sequence": 10,
                            "code": "A1",
                            "name": "PY Aspect One",
                            "level_ids": levels,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "sequence": 20,
                            "code": "A2",
                            "name": "PY Aspect Two",
                            "level_ids": levels,
                        },
                    ),
                ],
                "threshold_ids": [
                    (0, 0, {"min_total": 3, "status_id": self.eligible.id}),
                    (0, 0, {"min_total": 1, "status_id": self.revision.id}),
                ],
            }
        )

    def _create_artifact(self, activity_name):
        """Create a draft artifact of the school.

        :param activity_name: activity name of the artifact
        :return: the ``school_learning_artifact`` record
        """
        return self.env["school_learning_artifact"].create(
            {
                "school_id": self.school.id,
                "academic_year_id": self.year.id,
                "grade_class_id": self.grade_class.id,
                "activity_name": activity_name,
                "media_type": "photo",
                "user_id": self.env.ref("base.user_admin").id,
                "student_ids": [(6, 0, self.student.ids)],
                "learning_area_id": self.area.id,
                "category_id": self.category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
            }
        )

    @mute_logger("odoo.sql_db")
    def test_used_level_cannot_be_deleted(self):
        """Reject deleting a level that an answer already uses.

        Pure Python -- trigger P5 (L-22: ``psycopg2.IntegrityError`` is
        outside the 12 error types ``expect_error`` understands). The
        level is referenced with ``ondelete="restrict"``;
        ``mute_logger("odoo.sql_db")`` silences the PostgreSQL ERROR
        line that ``oca_checklog_odoo`` would otherwise report.
        """
        rubric = self._create_rubric(with_levels=True)
        artifact = self._create_artifact("PY Restrict")
        criterion = rubric.criterion_ids[0]
        level = criterion.level_ids[0]
        row = self.env["school_learning_artifact_score"].create(
            {"artifact_id": artifact.id, "criterion_id": criterion.id}
        )
        row.write({"level_id": level.id})
        with self.assertRaises(IntegrityError):
            with self.env.cr.savepoint():
                level.unlink()

    def _prepare_old_shape(self):
        """Build data shaped like the database before the upgrade.

        The rubric has two aspects with only a score range. One
        artifact is Curated and passed the ethics gate, one is On
        Progress with one given score and one empty score, and one is
        Curated and failed the gate with a reason and an assessor. The
        columns and tables that the upgrade removes are created again
        so that the script can read and drop them.

        :return: tuple of (rubric, done, open and fail artifacts)
        """
        env = self.env
        cr = env.cr
        admin = env.ref("base.user_admin")
        rubric = self._create_rubric(with_levels=False)
        artifacts = [
            self._create_artifact("PY Done"),
            self._create_artifact("PY Open"),
            self._create_artifact("PY Fail"),
        ]
        a_done, a_open, a_fail = artifacts
        for artifact in artifacts:
            for criterion in rubric.criterion_ids:
                env["school_learning_artifact_score"].create(
                    {"artifact_id": artifact.id, "criterion_id": criterion.id}
                )
        env["base"].flush()
        cr.execute(
            "UPDATE school_learning_artifact_rubric_criterion "
            "SET min_score = 1, "
            "max_score = CASE code WHEN 'A1' THEN 3 ELSE 2 END "
            "WHERE rubric_id = %s",
            (rubric.id,),
        )
        given = {
            (a_done.id, "A1"): 2,
            (a_done.id, "A2"): 1,
            (a_open.id, "A1"): 2,
        }
        for (artifact_id, code), value in given.items():
            cr.execute(
                "UPDATE school_learning_artifact_score s SET score = %s "
                "FROM school_learning_artifact_rubric_criterion c "
                "WHERE c.id = s.criterion_id AND c.code = %s "
                "AND s.artifact_id = %s",
                (value, code, artifact_id),
            )
        cr.execute(
            "CREATE TABLE school_learning_artifact_ethics_reason "
            "(id SERIAL PRIMARY KEY, name VARCHAR)"
        )
        cr.execute(
            "INSERT INTO school_learning_artifact_ethics_reason (name) "
            "VALUES ('Plagiarism') RETURNING id"
        )
        reason_id = cr.fetchone()[0]
        cr.execute(
            "ALTER TABLE school_learning_artifact ADD COLUMN ethics_reason_id "
            "INTEGER REFERENCES school_learning_artifact_ethics_reason (id)"
        )
        cr.execute(
            "ALTER TABLE school_learning_artifact "
            "ADD COLUMN ethics_assessor_id INTEGER"
        )
        cr.execute(
            "CREATE TABLE school_la_rubric_ethics_group_rel "
            "(rubric_id INTEGER, group_id INTEGER)"
        )
        cr.execute(
            "INSERT INTO school_la_rubric_ethics_group_rel VALUES (%s, %s)",
            (rubric.id, env.ref("base.group_user").id),
        )
        env.cache.invalidate()
        artifacts_rs = a_done | a_open | a_fail
        for field_name in ("total_score", "curation_status_id"):
            env.add_to_compute(artifacts_rs._fields[field_name], artifacts_rs)
        artifacts_rs.flush(["total_score", "curation_status_id"])
        cr.execute(
            "UPDATE school_learning_artifact SET state = 'done', "
            "ethics_result = 'pass', ethics_assessor_id = %s WHERE id = %s",
            (admin.id, a_done.id),
        )
        cr.execute(
            "UPDATE school_learning_artifact SET state = 'open' WHERE id = %s",
            (a_open.id,),
        )
        cr.execute(
            "UPDATE school_learning_artifact SET state = 'done', "
            "ethics_result = 'fail', ethics_assessor_id = %s, "
            "ethics_reason_id = %s, curation_status_id = %s WHERE id = %s",
            (admin.id, reason_id, self.rejected.id, a_fail.id),
        )
        env.cache.invalidate()
        return rubric, a_done, a_open, a_fail

    def _snapshot(self, artifacts):
        """Read the columns that the upgrade must not change.

        :param artifacts: the artifacts to read
        :return: list of row tuples
        """
        self.env.cr.execute(SNAPSHOT_SQL, (tuple(artifacts.ids),))
        return self.env.cr.fetchall()

    def _load_script(self):
        """Load the conversion script from its file.

        :return: the loaded module
        """
        path = os.path.join(get_module_path(MODULE), MIGRATION_PATH)
        spec = importlib.util.spec_from_file_location("post_migration_1_4_0", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def _gate_row(self, artifact):
        """Return the ethics gate row of an artifact.

        :param artifact: the artifact
        :return: the ``school_learning_artifact_score`` record
        """
        return artifact.score_ids.filtered(lambda r: r.aspect_type == "gate")

    def test_conversion_script(self):
        """Convert old shaped data without moving totals or statuses.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.4.0/post-migration.py``, which
        ``EVAL:`` cannot do). It checks the levels built from the
        score ranges, the rows linked to their level, the ethics gate
        aspect and rows, the removed columns and that a second run
        changes nothing.
        """
        rubric, a_done, a_open, a_fail = self._prepare_old_shape()
        artifacts = a_done | a_open | a_fail
        before = self._snapshot(artifacts)
        self.assertEqual([row[4] for row in before], ["pass", None, "fail"])
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.3.0")
        self.env.cache.invalidate()
        self.assertEqual(self._snapshot(artifacts), before)
        criteria = rubric.criterion_ids
        scored = criteria.filtered(lambda r: r.aspect_type == "score")
        self.assertEqual(
            scored.filtered(lambda r: r.code == "A1").level_ids.mapped("score"),
            [1, 2, 3],
        )
        self.assertEqual(
            scored.filtered(lambda r: r.code == "A2").level_ids.mapped("score"),
            [1, 2],
        )
        gate = criteria.filtered(lambda r: r.aspect_type == "gate")
        self.assertEqual(gate.code, "EG")
        self.assertEqual(gate.assessor_slot, "secondary")
        self.assertEqual(gate.assessor_group_ids, self.env.ref("base.group_user"))
        self.assertEqual(gate.level_ids.mapped("name"), ["Pass", "Fail"])
        self.assertEqual(gate.level_ids.mapped("is_fail"), [False, True])
        row_a1 = a_done.score_ids.filtered(lambda r: r.criterion_id.code == "A1")
        self.assertEqual(row_a1.level_id.score, 2)
        self.assertEqual(row_a1.level_text, "Score 2")
        self.assertEqual(row_a1.score, 2)
        open_rows = a_open.score_ids.filtered(lambda r: r.aspect_type == "score")
        self.assertEqual(open_rows.mapped("score"), [2, 0])
        self.assertEqual(len(open_rows.filtered("level_id")), 1)
        self.assertEqual(
            self.env.ref("base.user_admin"), self._gate_row(a_done).assessor_id
        )
        self.assertEqual(self._gate_row(a_done).level_id.name, "Pass")
        self.assertFalse(self._gate_row(a_open).level_id)
        fail_row = self._gate_row(a_fail)
        self.assertTrue(fail_row.level_id.is_fail)
        self.assertEqual(fail_row.level_text, "Fail: Plagiarism")
        self.assertEqual(fail_row.assessor_id, self.env.ref("base.user_admin"))
        self.env.cr.execute(
            "SELECT count(*) FROM information_schema.columns "
            "WHERE table_name = 'school_learning_artifact' "
            "AND column_name IN ('ethics_reason_id', 'ethics_assessor_id')"
        )
        self.assertEqual(self.env.cr.fetchone()[0], 0)
        self.env.cr.execute(
            "SELECT to_regclass('school_learning_artifact_ethics_reason')"
        )
        self.assertIsNone(self.env.cr.fetchone()[0])
        counts = (
            self.env[LEVEL_MODEL].search_count([]),
            self.env["school_learning_artifact_score"].search_count([]),
        )
        script.migrate(self.env.cr, "14.0.1.3.0")
        self.env.cache.invalidate()
        self.assertEqual(
            (
                self.env[LEVEL_MODEL].search_count([]),
                self.env["school_learning_artifact_score"].search_count([]),
            ),
            counts,
        )
        self.assertEqual(self._snapshot(artifacts), before)
