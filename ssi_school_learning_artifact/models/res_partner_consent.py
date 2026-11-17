# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


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
    is_current = fields.Boolean(
        string="Current",
        compute="_compute_is_current",
        search="_search_is_current",
        compute_sudo=True,
        help=(
            "Checked when this is the consent that applies: the latest "
            "event, by consent date and then by id, of the same contact, "
            "school and learning artifact usage. A consent of a purpose "
            "without a learning artifact usage is never current."
        ),
    )

    @api.depends(
        "partner_id",
        "school_id",
        "consent_date",
        "purpose_id.learning_artifact_usage",
    )
    def _compute_is_current(self):
        """Compute whether each consent is the one that applies.

        :return: None
        """
        partners = self.mapped("partner_id")
        current_ids = set()
        if partners:
            consents = self.sudo().search(
                [
                    ("partner_id", "in", partners.ids),
                    ("purpose_id.learning_artifact_usage", "!=", False),
                ]
            )
            current_ids = set(consents._select_current_consents().ids)
        for record in self:
            record.is_current = record.id in current_ids

    def _search_is_current(self, operator, value):
        """Search the consents by the current marker.

        :param operator: ``=`` or ``!=``
        :param value: boolean value to compare with
        :return: search domain on the ids of the current consents
        :raises UserError: when the operator or the value is not supported
        """
        if operator not in ("=", "!=") or not isinstance(value, bool):
            raise UserError(
                _("Only the operators = and != with a boolean value are supported.")
            )
        consents = self.sudo().search(
            [("purpose_id.learning_artifact_usage", "!=", False)]
        )
        current = consents._select_current_consents()
        positive = (operator == "=") == value
        return [("id", "in" if positive else "not in", current.ids)]

    def _select_current_consents(self):
        """Select the latest consent event of each contact, school and usage.

        The events are ordered by consent date and then by id, newest
        first, and the first event of every combination of contact,
        school and learning artifact usage is kept. The consents of a
        purpose without a usage are never selected. The consent state
        of a learning artifact uses the same rule.

        :return: subset of the recordset with the current consents
        """
        selected = self.browse()
        seen = set()
        for consent in self.sorted(key=lambda r: (r.consent_date, r.id), reverse=True):
            usage = consent.purpose_id.learning_artifact_usage
            key = (consent.partner_id.id, consent.school_id.id, usage)
            if not usage or key in seen:
                continue
            seen.add(key)
            selected |= consent
        return selected

    @api.model_create_multi
    def create(self, vals_list):
        """Create the consents and drop the stale current markers.

        A new event can replace the current consent of the same
        combination, so the cached markers of the other records are
        no longer valid.

        :param vals_list: list of values of the consents to create
        :return: the created consents
        """
        records = super().create(vals_list)
        self.invalidate_cache(["is_current"])
        return records
