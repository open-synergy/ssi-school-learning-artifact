# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

# Fixed order of the rows shown when the wizard is opened.
LEARNING_ARTIFACT_USAGES = [
    "inventory",
    "assessment",
    "publication",
    "promotion",
]


class RecordLearningArtifactConsent(models.TransientModel):
    """Wizard that records the artifact consents of a student at once.

    It is opened from the student form and shows one row per learning
    artifact usage. Every row with a consent type becomes one
    ``res.partner.consent`` record that shares the notice, the school, the
    date, the channel and the expiry date of the header. The wizard only
    creates consents; it never changes or removes an existing one.
    """

    _name = "record_learning_artifact_consent"
    _description = "Record Learning Artifact Consents"

    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        ondelete="cascade",
        help="The student whose artifact consents are recorded.",
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        related="student_id.contact_id",
        readonly=True,
        help="The contact of the student that gives the consents.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="cascade",
        help="The school unit the consents apply to.",
    )
    notice_id = fields.Many2one(
        string="Privacy Notice",
        comodel_name="partner_consent_notice",
        required=True,
        ondelete="cascade",
        help="The privacy notice version that the parent agreed to.",
    )
    consent_date = fields.Datetime(
        string="Consent Date",
        required=True,
        default=fields.Datetime.now,
        help="Date and time at which the consents were given.",
    )
    channel = fields.Selection(
        string="Channel",
        selection=[
            ("portal", "Portal"),
            ("manual", "Back Office"),
            ("import", "Import"),
        ],
        required=True,
        default="manual",
        help="Channel through which the consents were captured.",
    )
    date_expiry = fields.Date(
        string="Expiry Date",
        help=(
            "Optional date until which the consents are valid. It is "
            "informative and does not change the consent of an artifact."
        ),
    )
    line_ids = fields.One2many(
        string="Usages",
        comodel_name="record_learning_artifact_consent_line",
        inverse_name="wizard_id",
        help="One row per learning artifact usage.",
    )

    @api.model
    def default_get(self, fields_list):
        """Prefill the wizard with the student it was opened from.

        Reads the student from the ``active_id`` of the context (or from
        ``default_student_id``), takes the school of the student and
        builds one row per usage. A row gets its purpose when exactly one
        purpose covers the usage.

        :param fields_list: field names requested by the client
        :return: dict of default values
        """
        res = super().default_get(fields_list)
        student_id = res.get("student_id")
        context = self.env.context
        if not student_id and context.get("active_model") == "school_student":
            student_id = context.get("active_id")
        student = self.env["school_student"].browse(student_id or [])
        if student and "student_id" in fields_list:
            res["student_id"] = student.id
        if student and "school_id" in fields_list and not res.get("school_id"):
            res["school_id"] = student.school_id.id
        if "line_ids" in fields_list:
            res["line_ids"] = [
                (0, 0, self._prepare_default_line(usage))
                for usage in LEARNING_ARTIFACT_USAGES
            ]
        return res

    @api.model
    def _prepare_default_line(self, usage):
        """Prepare the values of the row of one usage.

        :param usage: key of the learning artifact usage
        :return: dict of values of the row
        """
        purposes = self.env["partner_consent_purpose"].search(
            [("learning_artifact_usage", "=", usage)]
        )
        return {
            "usage": usage,
            "purpose_id": purposes.id if len(purposes) == 1 else False,
        }

    def action_create_consents(self):
        """Create one consent per filled row, then close the dialog.

        :return: an ``ir.actions.act_window_close`` dict
        """
        for record in self.sudo():
            record._create_consents()
        return {"type": "ir.actions.act_window_close"}

    def _create_consents(self):
        """Validate every row, then create all the consents.

        Side effect: creates one ``res.partner.consent`` per filled row.
        Nothing is created when a row is not valid.

        :return: the created consent records
        """
        self.ensure_one()
        lines = self._validate_consents()
        consent_model = self.env["res.partner.consent"]
        return consent_model.create(
            [self._prepare_consent_values(line) for line in lines]
        )

    def _validate_consents(self):
        """Check the header and the rows before anything is created.

        :return: the rows that have a consent type
        :raises UserError: when the student has no contact, when no row has
            a consent type or when a filled row has no purpose
        :raises ValidationError: when a granted row has no consent level
        """
        self.ensure_one()
        if not self.partner_id:
            raise UserError(
                _(
                    """
Context: Record learning artifact consents
Database ID: %s
Problem: Student '%s' has no contact to record the consents for
Solution: Set the contact of the student, then open the wizard again
"""
                )
                % (self.student_id.id, self.student_id.display_name)
            )
        lines = self.line_ids.filtered(lambda line: line.consent_type)
        if not lines:
            raise UserError(
                _(
                    """
Context: Record learning artifact consents
Database ID: %s
Problem: No usage has a consent type
Solution: Choose Granted or Withdrawn on at least one usage
"""
                )
                % self.id
            )
        for line in lines:
            if not line.purpose_id:
                raise UserError(
                    _(
                        """
Context: Record learning artifact consents
Database ID: %s
Problem: The usage '%s' has a consent type but no purpose
Solution: Select the purpose of the usage or clear its consent type
"""
                    )
                    % (self.id, line.usage)
                )
            if line.consent_type == "grant" and not line.consent_level:
                raise ValidationError(
                    _(
                        """
Context: Record learning artifact consents
Database ID: %s
Problem: The granted usage '%s' has no consent level
Solution: Choose Full or Limited as the consent level of the usage
"""
                    )
                    % (self.id, line.usage)
                )
        return lines

    def _prepare_consent_values(self, line):
        """Prepare the values of the consent of one row.

        :param line: the wizard row of one usage
        :return: dict of values for ``res.partner.consent``
        """
        self.ensure_one()
        values = {
            "partner_id": self.partner_id.id,
            "school_id": self.school_id.id,
            "notice_id": self.notice_id.id,
            "consent_date": self.consent_date,
            "channel": self.channel,
            "date_expiry": self.date_expiry,
            "purpose_id": line.purpose_id.id,
            "consent_type": line.consent_type,
        }
        if line.consent_type == "grant":
            values["consent_level"] = line.consent_level
            if line.consent_level == "limited":
                values["limited_preference"] = line.limited_preference
        return values
