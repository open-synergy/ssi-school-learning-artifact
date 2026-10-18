# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolLearningArtifactScore(models.Model):
    """
    Represents the score that the curator gave to one aspect of one
    learning artifact. Whoever writes the score is recorded as the
    assessor together with the time of the scoring.
    """

    _name = "school_learning_artifact_score"
    _description = "School Learning Artifact Score"
    _order = "artifact_id, sequence, id"

    artifact_id = fields.Many2one(
        string="Learning Artifact",
        comodel_name="school_learning_artifact",
        required=True,
        ondelete="cascade",
        help="The learning artifact that this score belongs to.",
    )
    criterion_id = fields.Many2one(
        string="Aspect",
        comodel_name="school_learning_artifact_rubric_criterion",
        required=True,
        ondelete="restrict",
        help="The rubric aspect that this score rates.",
    )
    sequence = fields.Integer(
        string="Sequence",
        related="criterion_id.sequence",
        store=True,
        help="Order of the aspect in the rubric.",
    )
    score = fields.Integer(
        string="Score",
        help=(
            "The score given to the aspect. Zero means the aspect is " "not scored yet."
        ),
    )
    assessor_id = fields.Many2one(
        string="Assessor",
        comodel_name="res.users",
        readonly=True,
        help="The user who gave the score.",
    )
    date_score = fields.Datetime(
        string="Scored On",
        readonly=True,
        help="The time the score was given.",
    )

    @api.constrains("score", "criterion_id")
    def _check_score_range(self):
        """Keep each score inside the range of its aspect.

        :raises ValidationError: when a given score is below the
            minimum or above the maximum of the aspect
        """
        for record in self:
            criterion = record.criterion_id
            if record.score and not (
                criterion.min_score <= record.score <= criterion.max_score
            ):
                raise ValidationError(
                    _(
                        """
Context: Score learning artifact
Database ID: %s
Problem: Score %s is outside %s - %s of aspect %s
Solution: Enter a score within the range of the aspect
"""
                    )
                    % (
                        record.id,
                        record.score,
                        criterion.min_score,
                        criterion.max_score,
                        criterion.display_name,
                    )
                )

    def _check_assessor(self):
        """Reject scoring by a user outside the groups of the aspect.

        Nothing is checked for the superuser or for an aspect that
        lists no group.

        :raises UserError: when the active user may not score a row
        """
        if self.env.uid == SUPERUSER_ID:
            return
        user_groups = self.env.user.groups_id
        for record in self:
            allowed = record.criterion_id.assessor_group_ids
            if allowed and not (allowed & user_groups):
                raise UserError(
                    _(
                        """
Context: Score learning artifact
Database ID: %s
Problem: You are not allowed to score aspect %s
Solution: Ask a user in the assessor groups of the aspect to score it
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Create scores and record who gave them.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        for vals in vals_list:
            if vals.get("score"):
                vals["assessor_id"] = self.env.uid
                vals["date_score"] = fields.Datetime.now()
        records = super().create(vals_list)
        records.filtered("score")._check_assessor()
        return records

    def write(self, vals):
        """Write scores and record who gave them.

        :param vals: values to write
        :return: True
        """
        if "score" in vals:
            self._check_assessor()
            if vals["score"]:
                vals = dict(
                    vals,
                    assessor_id=self.env.uid,
                    date_score=fields.Datetime.now(),
                )
            else:
                vals = dict(vals, assessor_id=False, date_score=False)
        return super().write(vals)
