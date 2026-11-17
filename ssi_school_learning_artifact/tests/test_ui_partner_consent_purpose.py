# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiPartnerConsentPurpose(HttpSavepointCase):
    """Tour tests for the ``partner_consent_purpose`` usage instruction."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixture of the usage tour.

        One purpose without a learning artifact usage is created, with a
        school that the tour selects.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR LC Purpose Grade Type", "code": "/", "sequence": 10}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR LC Purpose School",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        cls.purpose = cls.env["partner_consent_purpose"].create(
            {
                "name": "TOUR LC Usage Purpose",
                "code": "TOURLCUP",
            }
        )

    def test_set_learning_artifact_usage(self):
        """Run the set usage tour for ``partner_consent_purpose``.

        IK: docs/partner_consent_purpose/01-set-learning-artifact-usage.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_partner_consent_purpose_set_learning_artifact_usage",
            login="admin",
        )
