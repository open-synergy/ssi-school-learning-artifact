# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolStudent(models.Model):  # pylint: disable=too-few-public-methods
    _name = "school_student"
    _inherit = ["school_student"]

    def action_open_learning_artifact_consent(self):
        """Open the data privacy consents of the contact of the student.

        New consents opened from here default to the contact, the
        school of the student and the back office channel.

        :return: window action of the consent log of the contact
        """
        self.ensure_one()
        action = self.env.ref(
            "ssi_school_learning_artifact.res_partner_consent_action"
        ).read()[0]
        action["domain"] = [("partner_id", "=", self.contact_id.id)]
        action["context"] = {
            "default_partner_id": self.contact_id.id,
            "default_school_id": self.school_id.id,
            "default_channel": "manual",
        }
        return action

    def action_open_record_learning_artifact_consent(self):
        """Open the wizard that records the artifact consents at once.

        The wizard shows one row per learning artifact usage and creates
        one consent per filled row for the contact of the student.

        :return: window action opening the wizard in a dialog
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Record Learning Artifact Consents",
            "res_model": "record_learning_artifact_consent",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_student_id": self.id,
                "default_school_id": self.school_id.id,
            },
        }
