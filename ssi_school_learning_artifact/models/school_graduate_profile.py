# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolGraduateProfile(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents a graduate profile of a school. A learning
    artifact takes the first active profile, by sequence, that
    covers the grade of its class.
    """

    _name = "school_graduate_profile"
    _inherit = ["mixin.master_data"]
    _description = "School Graduate Profile"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help=(
            "Display and selection order. When several profiles cover "
            "the same grade, the lowest sequence is chosen."
        ),
    )
    grade_ids = fields.Many2many(
        string="Grades",
        comodel_name="school_grade",
        help="The grades covered by this graduate profile.",
    )
