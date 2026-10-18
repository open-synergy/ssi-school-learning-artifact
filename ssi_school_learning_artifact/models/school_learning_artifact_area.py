# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactArea(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a learning area of a learning artifact: a subject,
    an activity area, a development area or a competition field.
    Learning areas are configured per school unit, so every school
    keeps its own list.
    """

    _name = "school_learning_artifact_area"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Area"

    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        help="The school unit that owns this learning area.",
    )
    area_type = fields.Selection(
        string="Area Type",
        selection=[
            ("subject", "Subject"),
            ("activity", "Activity Area"),
            ("development", "Development Area"),
            ("competition", "Competition Field"),
        ],
        required=True,
        help=(
            "Kind of the learning area: a subject, an activity area, "
            "a development area or a competition field."
        ),
    )
