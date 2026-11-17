# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PartnerConsentPurpose(models.Model):  # pylint: disable=too-few-public-methods
    _name = "partner_consent_purpose"
    _inherit = ["partner_consent_purpose"]

    # Maps a purpose of the data privacy consent to one usage of the
    # learning artifact. Purposes without a usage are ignored by the
    # consent aggregates of the artifact.
    learning_artifact_usage = fields.Selection(
        string="Learning Artifact Usage",
        selection=[
            ("inventory", "Inventory"),
            ("assessment", "Internal Assessment"),
            ("publication", "Publication"),
            ("promotion", "Promotion"),
        ],
        help=(
            "The usage of a learning artifact that this purpose covers. "
            "Leave it empty when the purpose does not concern learning "
            "artifacts."
        ),
    )
    # Schools the purpose applies to. An empty list means the purpose
    # applies to every school.
    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        relation="partner_consent_purpose_school_rel",
        column1="purpose_id",
        column2="school_id",
        help=(
            "The schools this purpose applies to. Leave it empty when the "
            "purpose applies to every school."
        ),
    )
