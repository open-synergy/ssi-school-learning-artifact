# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactRubric(HttpSavepointCase):
    """Tour test of the operating unit work instruction (rubric)."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the create tour.

        One operating unit is created for the tour to select. The tour
        session is ``admin``, a manager of operating units who sees the
        field Operating Unit.
        """
        super().setUpClass()
        partner = cls.env["res.partner"].create({"name": "TOUR OUM Unit Partner"})
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR OUM Unit",
                "code": "TOURRBCOUMU",
                "company_id": cls.env.ref("base.main_company").id,
                "partner_id": partner.id,
            }
        )
        cls.env["school_learning_artifact_curation_status"].create(
            {
                "name": "TOUR OUM Fail Status",
                "code": "TOUROUMFS",
                "category": "rejected",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_learning_artifact_rubric``.

        IK: docs/school_learning_artifact_rubric/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_operating_unit_"
            "school_learning_artifact_rubric_create",
            login="admin",
        )
