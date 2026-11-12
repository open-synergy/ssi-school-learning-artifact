# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactRubricTier(YamlTransactionCase):
    """Test the three tiers of the rubric choice of the artifact.

    The tiers combine the school criteria of the core with the
    operating unit of the artifact.
    """

    def setUp(self):
        """Create the units, the school and the rubric fixtures.

        :return: None
        """
        super().setUp()
        env = self.env
        self.unit_a = self._create_unit("RTRA")
        self.unit_b = self._create_unit("RTRB")
        grade_type = env["school_grade_type"].create(
            {"name": "RT Grade Type", "code": "/", "sequence": 10}
        )
        self.school = env["school"].create(
            {
                "name": "RT School",
                "code": "/",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, self.unit_a.ids)],
            }
        )
        grade = env["school_grade"].create(
            {"name": "RT Grade", "code": "/", "sequence": 10, "type_id": grade_type.id}
        )
        self.grade_class = env["school_grade_class"].create(
            {
                "name": "RT Class",
                "code": "/",
                "school_id": self.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        self.year = env["school_academic_year"].create(
            {
                "name": "RT Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        self.fail_status = env["school_learning_artifact_curation_status"].create(
            {"name": "RT Fail Status", "code": "/", "category": "rejected"}
        )

    def _create_unit(self, code):
        """Create an operating unit with its partner.

        :param code: code of the operating unit
        :return: the operating unit record
        """
        env = self.env
        partner = env["res.partner"].create({"name": "RT %s" % code})
        return env["operating.unit"].create(
            {
                "name": "RT %s" % code,
                "code": code,
                "company_id": env.ref("base.main_company").id,
                "partner_id": partner.id,
            }
        )

    def _create_rubric(self, name, schools=None, units=None):
        """Create a rubric.

        :param name: name of the rubric
        :param schools: school records the rubric lists, if any
        :param units: operating unit records of the rubric, if any
        :return: the rubric record
        """
        values = {
            "name": "RT %s" % name,
            "code": "/",
            "ethics_fail_status_id": self.fail_status.id,
        }
        if schools:
            values["school_ids"] = [(6, 0, schools.ids)]
        if units:
            values["operating_unit_ids"] = [(6, 0, units.ids)]
        return self.env["school_learning_artifact_rubric"].create(values)

    def _create_artifact(self, name):
        """Create an artifact of the school in operating unit A.

        :param name: activity name of the artifact
        :return: the artifact record
        """
        return self.env["school_learning_artifact"].create(
            {
                "school_id": self.school.id,
                "operating_unit_id": self.unit_a.id,
                "academic_year_id": self.year.id,
                "grade_class_id": self.grade_class.id,
                "activity_name": name,
                "media_type": "photo",
                "user_id": self.env.ref("base.user_admin").id,
            }
        )

    def test_rubric_tiers(self):
        """Pick the rubric by school and operating unit tier.

        Pure Python -- trigger P10 (L-11: the school link of the
        rubric exists only while the core keeps ``school_ids``, so
        the test must skip itself when the field is gone, which YAML
        cannot do). Tier 2 picks the rubric of the school without unit
        over the global one, tier 1 picks the rubric of the school and
        the unit over both, and the rubric of another unit is never
        picked.
        """
        env = self.env
        if "school_ids" not in env["school_learning_artifact_rubric"]._fields:
            self.skipTest("The core no longer limits the rubric by school.")
        school = self.school
        self._create_rubric("global")
        rubric_school = self._create_rubric("school", schools=school)
        self._create_rubric("school unit B", schools=school, units=self.unit_b)
        artifact_t2 = self._create_artifact("RT Activity 2")
        self.assertEqual(artifact_t2.rubric_id, rubric_school)
        rubric_unit = self._create_rubric(
            "school unit A", schools=school, units=self.unit_a
        )
        artifact_t1 = self._create_artifact("RT Activity 1")
        self.assertEqual(artifact_t1.rubric_id, rubric_unit)
        self.assertTrue(artifact_t2._is_rubric_stale())
        self.assertFalse(artifact_t1._is_rubric_stale())
