# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactCharacterIndicator(HttpSavepointCase):
    """Tour test for the character indicator work instruction."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the indicator tour.

        One school with a draft artifact tagged with a dominant
        sub-construct and an indicator of that sub-construct are
        created. ``user_id`` is set to ``base.user_admin`` because
        ``cls.env`` runs as SUPERUSER and the internal user record
        rule would otherwise hide the record from the tour session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR CI Grade Type",
                "code": "TOURCIGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR CI School",
                "code": "TOURCISC",
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR CI Grade",
                "code": "TOURCIGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR CI Class",
                "code": "TOURCICL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR CI Year",
                "code": "TOURCIAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR CI Student Contact"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR CI Student",
                "code": "TOURCIST",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )
        area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR CI Area",
                "code": "TOURCIAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR CI Category",
                "code": "TOURCICA",
            }
        )
        construct = cls.env["school_character_construct"].create(
            {"name": "TOUR CI Construct", "code": "TOUR-CI-CON"}
        )
        obj_subconstruct = cls.env["school_character_subconstruct"]
        cls.dominant = obj_subconstruct.create(
            {
                "name": "TOUR CI Dominant",
                "code": "TOUR-CI-DOM",
                "construct_id": construct.id,
            }
        )
        cls.indicator = cls.env["school_character_indicator"].create(
            {
                "name": "TOUR CI Indicator",
                "code": "TOUR-CI-IND",
                "construct_id": construct.id,
                "subconstruct_id": cls.dominant.id,
                "grade_status_ids": [
                    (
                        0,
                        0,
                        {
                            "grade_type_id": grade_type.id,
                            "grade_ids": [(6, 0, grade.ids)],
                            "status": "effective",
                        },
                    )
                ],
            }
        )
        cls.artifact = cls.env["school_learning_artifact"].create(
            {
                "school_id": cls.school.id,
                "academic_year_id": year.id,
                "grade_class_id": grade_class.id,
                "activity_name": "TOUR CI Activity",
                "media_type": "photo",
                "user_id": cls.admin.id,
                "student_ids": [(6, 0, student.ids)],
                "learning_area_id": area.id,
                "category_id": category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
                "primary_subconstruct_id": cls.dominant.id,
            }
        )

    def test_select_character_indicator(self):
        """Run the select indicator tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/13-select-character-indicator.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_character_school_learning_artifact_"
            "select_character_indicator",
            login="admin",
        )
