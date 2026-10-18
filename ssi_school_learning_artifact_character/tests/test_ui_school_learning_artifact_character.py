# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactCharacter(HttpSavepointCase):
    """Tour test for the character tag work instruction of the artifact."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the character tag tour.

        One school with a draft artifact and a construct with a dominant
        and a secondary sub-construct are created. ``user_id`` is set to
        ``base.user_admin`` because ``cls.env`` runs as SUPERUSER and the
        internal user record rule would otherwise hide the record from
        the tour session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR CT Grade Type",
                "code": "TOURCTGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR CT School",
                "code": "TOURCTSC",
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR CT Grade",
                "code": "TOURCTGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR CT Class",
                "code": "TOURCTCL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR CT Year",
                "code": "TOURCTAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR CT Student Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR CT Student",
                "code": "TOURCTST",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )
        area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR CT Area",
                "code": "TOURCTAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR CT Category",
                "code": "TOURCTCA",
            }
        )
        construct = cls.env["school_character_construct"].create(
            {"name": "TOUR CT Construct", "code": "TOUR-CT-CON"}
        )
        obj_subconstruct = cls.env["school_character_subconstruct"]
        cls.dominant = obj_subconstruct.create(
            {
                "name": "TOUR CT Dominant",
                "code": "TOUR-CT-DOM",
                "construct_id": construct.id,
            }
        )
        cls.secondary = obj_subconstruct.create(
            {
                "name": "TOUR CT Secondary",
                "code": "TOUR-CT-SEC",
                "construct_id": construct.id,
            }
        )
        cls.artifact = cls.env["school_learning_artifact"].create(
            {
                "school_id": cls.school.id,
                "academic_year_id": year.id,
                "grade_class_id": grade_class.id,
                "activity_name": "TOUR CT Activity",
                "media_type": "photo",
                "user_id": cls.admin.id,
                "student_ids": [(6, 0, student.ids)],
                "learning_area_id": area.id,
                "category_id": category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
            }
        )

    def test_tag_character(self):
        """Run the tag character tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/11-tag-character.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_character_school_learning_artifact_"
            "tag_character",
            login="admin",
        )
