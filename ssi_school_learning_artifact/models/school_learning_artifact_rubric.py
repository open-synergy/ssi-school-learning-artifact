# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactRubric(models.Model):
    """
    Represents the curation rubric of a learning artifact: the
    aspects that are scored, the thresholds that turn the total score
    into a curation status, the knockout and ethics outcomes, and the
    rules about who may assess. A rubric belongs to some schools; a
    rubric without schools is the fallback of every school that has
    no rubric of its own.
    """

    _name = "school_learning_artifact_rubric"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Rubric"

    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        relation="school_la_rubric_school_rel",
        column1="rubric_id",
        column2="school_id",
        help=(
            "Schools that use this rubric. Leave empty to make this "
            "the fallback rubric of the schools without a rubric."
        ),
    )
    criterion_ids = fields.One2many(
        string="Aspects",
        comodel_name="school_learning_artifact_rubric_criterion",
        inverse_name="rubric_id",
        help="The aspects that the curator scores.",
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
    ethics_assessor_group_ids = fields.Many2many(
        string="Ethics Assessor Groups",
        comodel_name="res.groups",
        relation="school_la_rubric_ethics_group_rel",
        column1="rubric_id",
        column2="group_id",
        help=(
            "Groups allowed to set the ethics result. Leave empty to "
            "let every user with access do it."
        ),
    )
    require_distinct_assessors = fields.Boolean(
        string="Require Distinct Assessors",
        default=False,
        help=(
            "If checked, nobody may assess both a primary and a "
            "secondary slot, the ethics gate counting as secondary."
        ),
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
