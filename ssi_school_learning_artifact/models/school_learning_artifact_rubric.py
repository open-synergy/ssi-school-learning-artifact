# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactRubric(models.Model):
    """
    Represents the curation rubric of a learning artifact: the
    aspects (scored aspects and ethics gate aspects, each with its
    levels), the thresholds that turn the total score into a curation
    status, the knockout and ethics outcomes, and the rules about who
    may assess. The core picks the first active rubric; the
    restriction per school is given by extension modules.
    """

    _name = "school_learning_artifact_rubric"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Rubric"

    criterion_ids = fields.One2many(
        string="Aspects",
        comodel_name="school_learning_artifact_rubric_criterion",
        inverse_name="rubric_id",
        help="The scored aspects and the ethics gate aspects.",
    )
    threshold_ids = fields.One2many(
        string="Thresholds",
        comodel_name="school_learning_artifact_rubric_threshold",
        inverse_name="rubric_id",
        help=(
            "The minimum total scores and the status each one gives. "
            "The highest minimum that the total reaches wins."
        ),
    )
    ethics_fail_status_id = fields.Many2one(
        string="Ethics Fail Status",
        comodel_name="school_learning_artifact_curation_status",
        required=True,
        ondelete="restrict",
        help="Status given to an artifact that fails the ethics gate.",
    )
    knockout_status_id = fields.Many2one(
        string="Knockout Status",
        comodel_name="school_learning_artifact_curation_status",
        ondelete="restrict",
        help=(
            "Status given to an artifact when an aspect scores at or "
            "below its knockout score."
        ),
    )
    require_distinct_assessors = fields.Boolean(
        string="Require Distinct Assessors",
        default=False,
        help=("If checked, nobody may assess both a primary and a " "secondary slot."),
    )
    forbid_creator_assessment = fields.Boolean(
        string="Forbid Creator Assessment",
        default=False,
        help=("If checked, the responsible user of the artifact may not " "assess it."),
    )
    max_revision = fields.Integer(
        string="Maximum Revision",
        default=1,
        help=("How many times an artifact that needs revision can be " "reopened."),
    )
