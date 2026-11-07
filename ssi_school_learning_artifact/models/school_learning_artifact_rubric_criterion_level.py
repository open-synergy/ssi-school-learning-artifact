# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolLearningArtifactRubricCriterionLevel(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents one level of a rubric aspect: a descriptive text that
    the assessor picks and the score it stands for. A level of an
    ethics gate aspect can be marked as failing the gate.
    """

    _name = "school_learning_artifact_rubric_criterion_level"
    _description = "School Learning Artifact Rubric Aspect Level"
    _order = "criterion_id, sequence, id"
    _rec_name = "name"

    criterion_id = fields.Many2one(
        string="Aspect",
        comodel_name="school_learning_artifact_rubric_criterion",
        required=True,
        ondelete="cascade",
        help="The rubric aspect that this level belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of the level in the aspect.",
    )
    score = fields.Integer(
        string="Score",
        help=(
            "The score that the level gives to a scored aspect. It is "
            "not used by an ethics gate aspect."
        ),
    )
    name = fields.Text(
        string="Description",
        required=True,
        help="The full text of the level that the assessor reads.",
    )
    is_fail = fields.Boolean(
        string="Fails the Gate",
        default=False,
        help=(
            "If checked, choosing this level fails the ethics gate. "
            "Only a level of an ethics gate aspect can fail it."
        ),
    )

    @api.constrains("is_fail", "criterion_id")
    def _check_is_fail_gate(self):
        """Allow the failing mark only on levels of a gate aspect.

        :raises ValidationError: when a level of a scored aspect is
            marked as failing the gate
        """
        for record in self:
            if record.is_fail and record.criterion_id.aspect_type != "gate":
                raise ValidationError(
                    _(
                        """
Context: Configure rubric aspect level
Database ID: %s
Problem: Level of scored aspect %s cannot fail the gate
Solution: Uncheck Fails the Gate or set the aspect type to Ethics Gate
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )
