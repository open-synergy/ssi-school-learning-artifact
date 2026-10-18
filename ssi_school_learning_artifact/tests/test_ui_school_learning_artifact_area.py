# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactArea(HttpSavepointCase):
    """Tour tests for the ``school_learning_artifact_area`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition data of the create tour.

        The school unit that owns the learning area.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR LA Area Grade Type",
                "code": "TOURLAAGT",
                "sequence": 10,
            }
        )
        cls.env["school"].create(
            {
                "name": "TOUR LA Area School",
                "code": "TOURLAAS",
                "grade_type_id": grade_type.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_learning_artifact_area``.

        IK: docs/school_learning_artifact_area/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_area_create",
            login="admin",
        )
