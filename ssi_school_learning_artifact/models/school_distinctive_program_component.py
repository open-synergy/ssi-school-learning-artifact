# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolDistinctiveProgramComponent(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents one component of a distinctive program. A learning
    artifact points to a primary and an optional secondary
    component. The abbreviation is used in the names of media
    files. Components are deleted together with their program.
    """

    _name = "school_distinctive_program_component"
    _inherit = ["mixin.master_data"]
    _description = "School Distinctive Program Component"

    abbreviation = fields.Char(
        string="Abbreviation",
        help="Short form of the component name, used in media file names.",
    )
    program_id = fields.Many2one(
        string="Program",
        comodel_name="school_distinctive_program",
        required=True,
        ondelete="cascade",
        help=(
            "The distinctive program this component belongs to. The "
            "component is deleted together with the program."
        ),
    )
