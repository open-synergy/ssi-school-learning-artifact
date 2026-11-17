# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import PropertyMock, patch

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactConsentWizard(YamlTransactionCase):
    """Test the wizard that records the four artifact consents at once.

    Runs the YAML scenarios covering the default rows, the creation of
    the consents, the skipped rows, the refused inputs and the access of
    the wizard, plus Python tests for the order of the rows and for the
    student without a contact.
    """

    def _create_student(self):
        """Create a school and a student with a contact.

        :return: the student record
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type for Consent Wizard", "code": "/", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School for Consent Wizard",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Contact Consent Wizard"})
        return self.env["school_student"].create(
            {
                "name": "Student for Consent Wizard",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )

    def test_school_learning_artifact_consent_wizard(self):
        """Run every consent wizard scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_consent_wizard.yaml")

    def test_action_open_record_learning_artifact_consent(self):
        """Assert the window action opened from the student form.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot assert the action dictionary).

        :return: None
        """
        student = self._create_student()
        action = student.action_open_record_learning_artifact_consent()
        self.assertEqual(action["res_model"], "record_learning_artifact_consent")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_student_id"], student.id)
        self.assertEqual(action["context"]["default_school_id"], student.school_id.id)

    def test_wizard_rows_follow_the_usage_order(self):
        """Assert the rows are created in the fixed usage order.

        Pure Python - trigger P3 (L-06: the comparison of one2many rows
        is a set, so YAML cannot assert their order).

        :return: None
        """
        student = self._create_student()
        wizard = (
            self.env["record_learning_artifact_consent"]
            .with_context(active_model="school_student", active_id=student.id)
            .create({"notice_id": self._create_notice().id})
        )
        self.assertEqual(wizard.student_id, student)
        self.assertEqual(
            wizard.line_ids.sorted("id").mapped("usage"),
            ["inventory", "assessment", "publication", "promotion"],
        )

    def _create_notice(self):
        """Create a privacy notice.

        :return: the notice record
        """
        return self.env["partner_consent_notice"].create(
            {
                "name": "Notice for Consent Wizard",
                "code": "/",
                "version": "1.0",
                "body": "Privacy notice text",
            }
        )

    def test_wizard_student_without_contact(self):
        """Assert the wizard refuses a student that has no contact.

        Pure Python - trigger P6 (L-15: no patch in YAML). The contact of a
        student is required, so the empty contact is simulated by patching
        the related field of the wizard.

        :return: None
        """
        student = self._create_student()
        purpose = self.env["partner_consent_purpose"].create(
            {
                "name": "Inventory Purpose for Consent Wizard",
                "code": "/",
                "learning_artifact_usage": "inventory",
            }
        )
        wizard = self.env["record_learning_artifact_consent"].create(
            {
                "student_id": student.id,
                "school_id": student.school_id.id,
                "notice_id": self._create_notice().id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "usage": "inventory",
                            "purpose_id": purpose.id,
                            "consent_type": "grant",
                            "consent_level": "full",
                        },
                    )
                ],
            }
        )
        empty_partner = self.env["res.partner"]
        with patch.object(
            type(wizard),
            "partner_id",
            new_callable=PropertyMock,
            return_value=empty_partner,
        ):
            with self.assertRaises(UserError):
                wizard.action_create_consents()
        self.assertFalse(
            self.env["res.partner.consent"].search(
                [("partner_id", "=", student.contact_id.id)]
            )
        )
