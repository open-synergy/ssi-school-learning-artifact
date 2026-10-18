# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolCharacterIndicator(models.Model):
    _name = "school_character_indicator"
    _inherit = [
        "school_character_indicator",
    ]

    # Adds the status of the indicator per grade type.
    grade_status_ids = fields.One2many(
        string="Grade Statuses",
        comodel_name="school_character_indicator_grade_status",
        inverse_name="indicator_id",
        help=(
            "The status of this indicator per grade type. Leave empty "
            "when the school does not filter character tags by grade "
            "type."
        ),
    )
