# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolLearningArtifactRubricCriterion(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents one aspect of a rubric: either a scored aspect or an
    ethics gate aspect. The aspect lists the levels that the assessor
    can pick; the score range follows from those levels. It also holds
    the knockout score and the groups allowed to assess it.
    """

    _name = "school_learning_artifact_rubric_criterion"
    _description = "School Learning Artifact Rubric Aspect"
    _order = "rubric_id, sequence, id"

    rubric_id = fields.Many2one(
        string="Rubric",
        comodel_name="school_learning_artifact_rubric",
        required=True,
        ondelete="cascade",
        help="The rubric that this aspect belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of the aspect in the rubric.",
    )
    code = fields.Char(
        string="Code",
        required=True,
        help="Short code of the aspect, for example A1.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the aspect.",
    )
    description = fields.Text(
        string="Description",
        help="Explanation of how to score the aspect.",
    )
    aspect_type = fields.Selection(
        string="Aspect Type",
        selection=[
            ("score", "Scored Aspect"),
            ("gate", "Ethics Gate"),
        ],
        default="score",
        required=True,
        help=(
            "A scored aspect gives a score to the total. An ethics "
            "gate aspect passes or fails the artifact."
        ),
    )
    level_ids = fields.One2many(
        string="Levels",
        comodel_name="school_learning_artifact_rubric_criterion_level",
        inverse_name="criterion_id",
        help="The levels that the assessor can pick for this aspect.",
    )
    min_score = fields.Integer(
        string="Minimum Score",
        compute="_compute_min_score",
        store=True,
        compute_sudo=True,
        help="Lowest score among the levels of this aspect.",
    )
    max_score = fields.Integer(
        string="Maximum Score",
        compute="_compute_max_score",
        store=True,
        compute_sudo=True,
        help="Highest score among the levels of this aspect.",
    )
    knockout_score = fields.Integer(
        string="Knockout Score",
        default=0,
        help=(
            "A score at or below this value knocks the artifact out. "
            "Zero means the aspect never knocks out. It is ignored by "
            "an ethics gate aspect."
        ),
    )
    assessor_slot = fields.Selection(
        string="Assessor Slot",
        selection=[
            ("primary", "Primary Assessor"),
            ("secondary", "Secondary Assessor"),
        ],
        default="primary",
        required=True,
        help="Which assessor slot assesses this aspect.",
    )
    assessor_group_ids = fields.Many2many(
        string="Assessor Groups",
        comodel_name="res.groups",
        relation="school_la_criterion_group_rel",
        column1="criterion_id",
        column2="group_id",
        help=(
            "Groups allowed to assess this aspect. Leave empty to let "
            "every user with access do it."
        ),
    )

    @api.depends("level_ids.score")
    def _compute_min_score(self):
        """Take the lowest score among the levels of the aspect.

        The result is zero for an aspect without levels.
        """
        for record in self:
            result = 0
            scores = record.level_ids.mapped("score")
            if scores:
                result = min(scores)
            record.min_score = result

    @api.depends("level_ids.score")
    def _compute_max_score(self):
        """Take the highest score among the levels of the aspect.

        The result is zero for an aspect without levels.
        """
        for record in self:
            result = 0
            scores = record.level_ids.mapped("score")
            if scores:
                result = max(scores)
            record.max_score = result
