# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactRubricCriterion(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents one scored aspect of a rubric: its score range, the
    knockout score and the groups allowed to score it.
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
    min_score = fields.Integer(
        string="Minimum Score",
        default=1,
        help="Lowest score that can be given to this aspect.",
    )
    max_score = fields.Integer(
        string="Maximum Score",
        default=3,
        help="Highest score that can be given to this aspect.",
    )
    knockout_score = fields.Integer(
        string="Knockout Score",
        default=0,
        help=(
            "A score at or below this value knocks the artifact out. "
            "Zero means the aspect never knocks out."
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
        help="Which assessor slot scores this aspect.",
    )
    assessor_group_ids = fields.Many2many(
        string="Assessor Groups",
        comodel_name="res.groups",
        relation="school_la_criterion_group_rel",
        column1="criterion_id",
        column2="group_id",
        help=(
            "Groups allowed to score this aspect. Leave empty to let "
            "every user with access do it."
        ),
    )
