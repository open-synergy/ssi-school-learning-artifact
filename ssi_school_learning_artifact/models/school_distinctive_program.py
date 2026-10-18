# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolDistinctiveProgram(models.Model):  # pylint: disable=too-few-public-methods
    """
    Represents the distinctive program (value proposition) of a
    school branch. A program is configured per branch and is
    inherited by every school unit of that branch. Its components
    are the choices offered on a learning artifact.
    """

    _name = "school_distinctive_program"
    _inherit = ["mixin.master_data"]
    _description = "School Distinctive Program"

    abbreviation = fields.Char(
        string="Abbreviation",
        help="Short form of the program name.",
    )
    branch_id = fields.Many2one(
        string="Branch",
        comodel_name="school_branch",
        required=True,
        ondelete="restrict",
        help=(
            "The branch that owns this program. Every school unit of "
            "the branch inherits it."
        ),
    )
    component_ids = fields.One2many(
        string="Components",
        comodel_name="school_distinctive_program_component",
        inverse_name="program_id",
        help="The components that make up this program.",
    )
