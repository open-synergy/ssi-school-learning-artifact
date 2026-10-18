# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactPhase(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a learning phase that a learning artifact can
    cover. Whether a school requires a phase is decided by the
    configuration of the school. A phase can be limited to some
    schools or left open to all schools.
    """

    _name = "school_learning_artifact_phase"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Phase"

    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        help=(
            "Schools that can use this phase. Leave empty to make the "
            "phase available to every school."
        ),
    )
