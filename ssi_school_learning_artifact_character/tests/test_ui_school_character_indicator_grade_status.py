# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolCharacterIndicatorGradeStatus(HttpSavepointCase):
    """Tour test for the grade status work instruction of the indicator."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the grade status tour.

        One construct with a sub-construct, an indicator of that
        sub-construct and a grade type are created.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR GS Grade Type",
                "code": "TOURGSGT",
                "sequence": 10,
            }
        )
        cls.construct = cls.env["school_character_construct"].create(
            {"name": "TOUR GS Construct", "code": "TOUR-GS-CON"}
        )
        cls.subconstruct = cls.env["school_character_subconstruct"].create(
            {
                "name": "TOUR GS Sub-construct",
                "code": "TOUR-GS-SUB",
                "construct_id": cls.construct.id,
            }
        )
        cls.indicator = cls.env["school_character_indicator"].create(
            {
                "name": "TOUR GS Indicator",
                "code": "TOUR-GS-IND",
                "construct_id": cls.construct.id,
                "subconstruct_id": cls.subconstruct.id,
            }
        )

    def test_set_grade_status(self):
        """Run the set grade status tour for the indicator.

        IK: docs/school_character_indicator/01-set-grade-status.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_character_school_character_indicator_"
            "set_grade_status",
            login="admin",
        )
