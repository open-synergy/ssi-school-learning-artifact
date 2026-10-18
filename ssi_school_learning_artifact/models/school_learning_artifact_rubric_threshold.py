# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactRubricThreshold(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents one threshold of a rubric: a minimum total score and
    the curation status it gives.
    """

    _name = "school_learning_artifact_rubric_threshold"
    _description = "School Learning Artifact Rubric Threshold"
    _order = "rubric_id, min_total desc, id"

    rubric_id = fields.Many2one(
        string="Rubric",
        comodel_name="school_learning_artifact_rubric",
        required=True,
        ondelete="cascade",
        help="The rubric that this threshold belongs to.",
    )
    min_total = fields.Integer(
        string="Minimum Total",
        required=True,
        help="Lowest total score that reaches this threshold.",
    )
    status_id = fields.Many2one(
        string="Status",
        comodel_name="school_learning_artifact_curation_status",
        required=True,
        ondelete="restrict",
        help="Status given when the total score reaches this threshold.",
    )
