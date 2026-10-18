# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactRubric(HttpSavepointCase):
    """Tour tests for the rubric work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixture of the create tour.

        The rubric requires an Ethics Fail Status, so one curation
        status is created for the tour to pick.
        """
        super().setUpClass()
        cls.env["school_learning_artifact_curation_status"].create(
            {
                "name": "TOUR Fail Status",
                "code": "TOURFAILST",
                "category": "rejected",
            }
        )

    def test_create(self):
        """Run the create tour for the rubric master.

        IK: docs/school_learning_artifact_rubric/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "rubric_create",
            login="admin",
        )
