# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class School(models.Model):  # pylint: disable=too-few-public-methods
    _name = "school"
    _inherit = ["school"]

    learning_artifact_link_prefix = fields.Char(
        string="Learning Artifact Link Prefix",
        help=(
            "Required beginning of the link of a learning artifact "
            "of this school, for example the URL of a shared folder. "
            "Leave empty to accept any link."
        ),
    )
    learning_artifact_require_component = fields.Boolean(
        string="Learning Artifact Requires Component",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a primary component before it can be submitted."
        ),
    )
    learning_artifact_require_dimension = fields.Boolean(
        string="Learning Artifact Requires Dimension",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a dimension before it can be submitted."
        ),
    )
    learning_artifact_require_phase = fields.Boolean(
        string="Learning Artifact Requires Phase",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a phase before it can be submitted."
        ),
    )
