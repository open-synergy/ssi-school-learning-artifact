# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolGraduateProfile(HttpSavepointCase):
    """Tour test of the operating unit work instruction (profile)."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the create tour.

        One operating unit is created for the tour to select. The tour
        session is ``admin``, a manager of operating units who sees the
        field Operating Unit.
        """
        super().setUpClass()
        partner = cls.env["res.partner"].create({"name": "TOUR OUM Profile Partner"})
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR OUM Profile Unit",
                "code": "TOURGPOUMU",
                "company_id": cls.env.ref("base.main_company").id,
                "partner_id": partner.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_graduate_profile``.

        IK: docs/school_graduate_profile/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_operating_unit_"
            "school_graduate_profile_create",
            login="admin",
        )
