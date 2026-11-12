# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_school_learning_artifact"
MIGRATION_PATH = os.path.join(
    "migrations",
    "14.0.1.7.0",
    "post-migration.py",
)


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactShowcaseMigration(YamlTransactionCase):
    """Test the showcase stage recompute of the 14.0.1.7.0 upgrade.

    Covers the migration script, which YAML scenarios cannot load from
    its file.
    """

    def setUp(self):
        """Create the school, the students and the consent of the tests.

        :return: None
        """
        super().setUp()
        env = self.env
        grade_type = env["school_grade_type"].create(
            {"name": "SM Grade Type", "code": "/", "sequence": 10}
        )
        branch = env["school_branch"].create({"name": "SM Branch", "code": "/"})
        self.school = env["school"].create(
            {
                "name": "SM School",
                "code": "/",
                "grade_type_id": grade_type.id,
                "branch_id": branch.id,
            }
        )
        grade = env["school_grade"].create(
            {"name": "SM Grade", "code": "/", "sequence": 10, "type_id": grade_type.id}
        )
        self.grade_class = env["school_grade_class"].create(
            {
                "name": "SM Class",
                "code": "/",
                "school_id": self.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        self.year = env["school_academic_year"].create(
            {
                "name": "SM Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        self.area = env["school_learning_artifact_area"].create(
            {
                "name": "SM Area",
                "code": "/",
                "school_id": self.school.id,
                "area_type": "subject",
            }
        )
        self.category = env["school_learning_artifact_category"].create(
            {"name": "SM Category", "code": "/"}
        )
        self.stage = env["school_learning_artifact_showcase_stage"].create(
            {"name": "SM Stage", "code": "/", "sequence": 10}
        )

    def _create_artifact(self, name, with_consent):
        """Create a draft artifact of a new student.

        :param name: name used for the student and the activity
        :param with_consent: when True the student grants a full
            publication consent
        :return: the ``school_learning_artifact`` record
        """
        env = self.env
        contact = env["res.partner"].create({"name": "SM Contact %s" % name})
        student = env["school_student"].create(
            {
                "name": "SM Student %s" % name,
                "code": "/",
                "contact_id": contact.id,
                "school_id": self.school.id,
            }
        )
        if with_consent:
            notice = env["partner_consent_notice"].create(
                {
                    "name": "SM Notice",
                    "code": "/",
                    "version": "1.0",
                    "body": "Privacy notice text",
                }
            )
            purpose = env["partner_consent_purpose"].create(
                {
                    "name": "SM Purpose",
                    "code": "/",
                    "learning_artifact_usage": "publication",
                }
            )
            env["res.partner.consent"].create(
                {
                    "partner_id": contact.id,
                    "school_id": self.school.id,
                    "notice_id": notice.id,
                    "purpose_id": purpose.id,
                    "consent_type": "grant",
                    "consent_date": "2026-10-01 08:00:00",
                    "channel": "manual",
                    "consent_level": "full",
                }
            )
        return env["school_learning_artifact"].create(
            {
                "school_id": self.school.id,
                "academic_year_id": self.year.id,
                "grade_class_id": self.grade_class.id,
                "activity_name": "SM Activity %s" % name,
                "media_type": "photo",
                "user_id": env.ref("base.user_admin").id,
                "student_ids": [(6, 0, student.ids)],
                "learning_area_id": self.area.id,
                "category_id": self.category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
            }
        )

    def _load_script(self):
        """Load the recompute script from its file.

        :return: the loaded module
        """
        path = os.path.join(get_module_path(MODULE), MIGRATION_PATH)
        spec = importlib.util.spec_from_file_location("post_migration_1_7_0", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_recompute_showcase_stage(self):
        """Take off the board only the artifact without a showcase consent.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.7.0/post-migration.py``, which
        ``EVAL:`` cannot do). Two artifacts sit on a stage with a
        passing ethics gate, as old data does: the one whose student
        gave no publication consent loses the stage, the other keeps
        it, and a second run changes nothing.
        """
        art_ok = self._create_artifact("ok", True)
        art_bad = self._create_artifact("bad", False)
        artifacts = art_ok | art_bad
        self.env.cr.execute(
            "UPDATE school_learning_artifact SET showcase_stage_id = %s, "
            "ethics_result = 'pass' WHERE id IN %s",
            (self.stage.id, tuple(artifacts.ids)),
        )
        self.env.cache.invalidate()
        self.assertEqual(artifacts.mapped("showcase_stage_id"), self.stage)
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.6.0")
        self.env.cache.invalidate()
        self.assertEqual(art_ok.showcase_stage_id, self.stage)
        self.assertFalse(art_bad.showcase_stage_id)
        script.migrate(self.env.cr, "14.0.1.6.0")
        self.env.cache.invalidate()
        self.assertEqual(art_ok.showcase_stage_id, self.stage)
        self.assertFalse(art_bad.showcase_stage_id)
