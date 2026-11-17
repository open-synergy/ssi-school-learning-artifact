# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import ValidationError
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactCharacterOnchange(YamlTransactionCase):
    """Test the character indicators while the tags are not saved yet.

    The YAML scenarios cannot add a record to a many2many field of a
    form, so these cases run the ``Form`` API in pure Python. They
    prove that the allowed indicators follow the tags chosen in the
    form before the artifact is saved, and that the indicator
    constraint holds for a record that is not saved yet.
    """

    def setUp(self):
        """Create the school data, the character master and an artifact.

        Two sub-constructs with one indicator each are created. The
        artifact is saved without any character tag.

        :return: None
        """
        super().setUp()
        env = self.env
        self.admin = env.ref("base.user_admin")
        grade_type = env["school_grade_type"].create(
            {"name": "OC Grade Type", "code": "/", "sequence": 10}
        )
        school = env["school"].create(
            {"name": "OC School", "code": "/", "grade_type_id": grade_type.id}
        )
        grade = env["school_grade"].create(
            {"name": "OC Grade", "code": "/", "sequence": 10, "type_id": grade_type.id}
        )
        grade_class = env["school_grade_class"].create(
            {
                "name": "OC Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "OC Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        area = env["school_learning_artifact_area"].create(
            {
                "name": "OC Area",
                "code": "/",
                "school_id": school.id,
                "area_type": "subject",
            }
        )
        category = env["school_learning_artifact_category"].create(
            {"name": "OC Category", "code": "/"}
        )
        contact = env["res.partner"].create({"name": "OC Contact"})
        student = env["school_student"].create(
            {
                "name": "OC Student",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        construct = env["school_character_construct"].create(
            {"name": "OC Construct", "code": "OC-CON"}
        )
        obj_subconstruct = env["school_character_subconstruct"]
        self.sub_a = obj_subconstruct.create(
            {"name": "OC Sub A", "code": "OC-SA", "construct_id": construct.id}
        )
        self.sub_b = obj_subconstruct.create(
            {"name": "OC Sub B", "code": "OC-SB", "construct_id": construct.id}
        )
        obj_indicator = env["school_character_indicator"]
        self.ind_a = obj_indicator.create(
            {
                "name": "OC Indicator A",
                "code": "OC-IA",
                "construct_id": construct.id,
                "subconstruct_id": self.sub_a.id,
            }
        )
        self.ind_b = obj_indicator.create(
            {
                "name": "OC Indicator B",
                "code": "OC-IB",
                "construct_id": construct.id,
                "subconstruct_id": self.sub_b.id,
            }
        )
        self.artifact = env["school_learning_artifact"].create(
            {
                "school_id": school.id,
                "academic_year_id": year.id,
                "grade_class_id": grade_class.id,
                "activity_name": "OC Activity",
                "media_type": "photo",
                "user_id": self.admin.id,
                "student_ids": [(6, 0, student.ids)],
                "learning_area_id": area.id,
                "category_id": category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
            }
        )

    def _open_form(self):
        """Open the form of the artifact as the administrator.

        :return: the ``Form`` of the artifact
        """
        return Form(self.artifact.with_user(self.admin))

    def test_dominant_indicators_follow_tag_before_save(self):
        """Dominant indicators appear as soon as the tag is picked.

        Pure Python -- trigger P3 (L-06: YAML cannot add a record to
        a many2many field of a form nor assert its members before
        the save; L-20).

        :return: None
        """
        form = self._open_form()
        form.dominant_subconstruct_ids.add(self.sub_a)
        self.assertEqual(
            form.allowed_dominant_indicator_ids[:].ids,
            self.ind_a.ids,
            "Only the indicator of the picked tag must be allowed",
        )
        form.save()
        self.assertEqual(self.artifact.allowed_dominant_indicator_ids, self.ind_a)

    def test_secondary_indicators_follow_tag_before_save(self):
        """Secondary indicators appear as soon as the tag is picked.

        Pure Python -- trigger P3 (L-06: YAML cannot add a record to
        a many2many field of a form nor assert its members before
        the save; L-20).

        :return: None
        """
        form = self._open_form()
        form.secondary_subconstruct_ids.add(self.sub_b)
        self.assertEqual(
            form.allowed_secondary_indicator_ids[:].ids,
            self.ind_b.ids,
            "Only the indicator of the picked tag must be allowed",
        )
        form.save()
        self.assertEqual(self.artifact.allowed_secondary_indicator_ids, self.ind_b)

    def test_changing_tag_of_saved_artifact(self):
        """The allowed indicators follow a tag changed on a saved record.

        Pure Python -- trigger P3 (L-06: YAML cannot remove or add a
        record of a many2many field of a form; L-20).

        :return: None
        """
        self.artifact.write({"dominant_subconstruct_ids": [(6, 0, self.sub_a.ids)]})
        self.assertEqual(self.artifact.allowed_dominant_indicator_ids, self.ind_a)
        form = self._open_form()
        form.dominant_subconstruct_ids.remove(id=self.sub_a.id)
        self.assertEqual(
            form.allowed_dominant_indicator_ids[:].ids,
            [],
            "Removing the tag must empty the allowed indicators",
        )
        form.dominant_subconstruct_ids.add(self.sub_b)
        self.assertEqual(
            form.allowed_dominant_indicator_ids[:].ids,
            self.ind_b.ids,
            "The indicator of the new tag must be allowed",
        )

    def test_indicator_constraint_on_unsaved_record(self):
        """The indicator constraint judges a record that is not saved.

        An indicator of the tag passes and an indicator of another
        tag is rejected, as when the constraint is called while the
        values are still the ones of an onchange.

        Pure Python -- trigger P3 (L-06: the records of an unsaved
        record hold new ids, which YAML cannot build; L-20).

        :return: None
        """
        values = {
            "dominant_subconstruct_ids": [(6, 0, self.sub_a.ids)],
            "dominant_indicator_ids": [(6, 0, self.ind_a.ids)],
        }
        record = self.artifact.new(values, origin=self.artifact)
        record._check_character_indicator()
        values["dominant_indicator_ids"] = [(6, 0, self.ind_b.ids)]
        record = self.artifact.new(values, origin=self.artifact)
        with self.assertRaises(ValidationError):
            record._check_character_indicator()
