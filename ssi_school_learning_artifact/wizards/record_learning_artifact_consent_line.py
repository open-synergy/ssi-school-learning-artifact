# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RecordLearningArtifactConsentLine(models.TransientModel):
    """One usage row of the wizard that records the artifact consents.

    The wizard creates one row per learning artifact usage when it is
    opened. A row with a consent type becomes one data privacy consent
    record; a row without a consent type is skipped.
    """

    _name = "record_learning_artifact_consent_line"
    _description = "Record Learning Artifact Consent Line"

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="record_learning_artifact_consent",
        required=True,
        ondelete="cascade",
        help="The wizard this row belongs to.",
    )
    usage = fields.Selection(
        string="Usage",
        selection=[
            ("inventory", "Inventory"),
            ("assessment", "Internal Assessment"),
            ("publication", "Publication"),
            ("promotion", "Promotion"),
        ],
        readonly=True,
        help="The usage of a learning artifact that this row covers.",
    )
    purpose_id = fields.Many2one(
        string="Purpose",
        comodel_name="partner_consent_purpose",
        ondelete="restrict",
        help=(
            "The consent purpose of the usage. It is filled in when exactly "
            "one purpose covers the usage."
        ),
    )
    consent_type = fields.Selection(
        string="Consent Type",
        selection=[
            ("grant", "Granted"),
            ("withdraw", "Withdrawn"),
        ],
        help=(
            "Whether the consent of the usage is granted or withdrawn. "
            "Leave it empty to skip this usage."
        ),
    )
    consent_level = fields.Selection(
        string="Consent Level",
        selection=[
            ("full", "Full"),
            ("limited", "Limited"),
        ],
        help="Whether the granted consent is full or limited.",
    )
    limited_preference = fields.Text(
        string="Limited Preference",
        help="What the data subject allows when the consent level is limited.",
    )
