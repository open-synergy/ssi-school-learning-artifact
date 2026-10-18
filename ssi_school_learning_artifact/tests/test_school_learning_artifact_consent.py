# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactConsent(YamlTransactionCase):
    """Test the parental consent of the Learning Artifact.

    Runs the YAML scenarios covering the consent aggregates per usage,
    the students who limit or refuse the publication, the consents of
    other schools and of purposes without a usage, the submit gate on
    the inventory consent, and the immutability of the consent log.
    """

    def test_school_learning_artifact_consent(self):
        """Run every consent scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_consent.yaml")

    def test_action_open_learning_artifact_consent(self):
        """Assert the window action opened from the student form.

        Pure Python - trigger P1 (L-01: the ``call`` action discards the
        return value, so YAML cannot assert the action dictionary).

        :return: None
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type for Consent Action", "code": "/", "sequence": 10}
        )
        school = self.env["school"].create(
            {
                "name": "School for Consent Action",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Contact Consent Action"})
        student = self.env["school_student"].create(
            {
                "name": "Student for Consent Action",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        action = student.action_open_learning_artifact_consent()
        self.assertEqual(action["res_model"], "res.partner.consent")
        self.assertEqual(action["domain"], [("partner_id", "=", contact.id)])
        self.assertEqual(action["context"]["default_partner_id"], contact.id)
        self.assertEqual(action["context"]["default_school_id"], school.id)
        self.assertEqual(action["context"]["default_channel"], "manual")
