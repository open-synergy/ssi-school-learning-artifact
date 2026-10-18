# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerConsent(models.Model):  # pylint: disable=too-few-public-methods
    _name = "res.partner.consent"
    _inherit = ["res.partner.consent"]

    # The records stay immutable: these fields are filled when the
    # consent event is created.
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        ondelete="restrict",
        help=(
            "The school unit this consent applies to. Leave it empty for "
            "a consent that does not concern a school."
        ),
    )
    consent_level = fields.Selection(
        string="Consent Level",
        selection=[
            ("full", "Full"),
            ("limited", "Limited"),
        ],
        default="full",
        help=(
            "Whether the granted consent is full or limited. A limited "
            "consent follows the preference written in Limited Preference."
        ),
    )
    limited_preference = fields.Text(
        string="Limited Preference",
        help="What the data subject allows when the consent level is limited.",
    )
    date_expiry = fields.Date(
        string="Expiry Date",
        help=(
            "Optional date until which the consent is valid. It is "
            "informative and does not change the consent of an artifact."
        ),
    )
