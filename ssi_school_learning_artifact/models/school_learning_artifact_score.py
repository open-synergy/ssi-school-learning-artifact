# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolLearningArtifactScore(models.Model):
    """
    Represents the answer that the curator gave to one aspect of one
    learning artifact: the level picked among the levels of the aspect.
    The score and the text of the level are copied when the level is
    picked, so editing the level later does not change a given answer.
    Whoever picks the level is recorded as the assessor together with
    the time of the assessment.
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
    aspect_type = fields.Selection(
        string="Aspect Type",
        related="criterion_id.aspect_type",
        store=True,
        help="Whether the aspect is scored or is an ethics gate.",
    )
    gate_source = fields.Selection(
        string="Gate Source",
        related="criterion_id.gate_source",
        help="Where the level of the aspect comes from.",
    )
    level_id = fields.Many2one(
        string="Level",
        comodel_name="school_learning_artifact_rubric_criterion_level",
        domain="[('criterion_id', '=', criterion_id)]",
        ondelete="restrict",
        compute="_compute_level_id",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "The level picked for the aspect. Empty means the aspect "
            "is not assessed yet. For an aspect that takes its level "
            "from the inventory consent, the system picks it and it "
            "follows the consent of the students."
        ),
    )
    level_text = fields.Text(
        string="Level Text",
        readonly=True,
        compute="_compute_level_text",
        store=True,
        compute_sudo=True,
        help=(
            "Copy of the text of the picked level, taken when the " "level was picked."
        ),
    )
    score = fields.Integer(
        string="Score",
        compute="_compute_score",
        store=True,
        compute_sudo=True,
        help=(
            "The score of the picked level, taken when the level was "
            "picked. Zero means the aspect is not assessed yet."
        ),
    )
    assessor_id = fields.Many2one(
        string="Assessor",
        comodel_name="res.users",
        readonly=True,
        help="The user who picked the level.",
    )
    date_score = fields.Datetime(
        string="Scored On",
        readonly=True,
        help="The time the level was picked.",
    )

    @api.depends(
        "criterion_id.gate_source",
        "artifact_id.inventory_consent",
        "criterion_id.level_ids.is_fail",
        "criterion_id.level_ids.sequence",
    )
    def _compute_level_id(self):
        """Pick the level of an aspect that follows the inventory consent.

        A full or limited inventory consent gives the first passing
        level, any other consent (refused, not recorded, or no student)
        gives the first failing level. The first level is the one with
        the lowest sequence. A manual aspect keeps the stored level.
        """
        for record in self:
            result = record.level_id
            criterion = record.criterion_id
            if criterion.gate_source == "inventory_consent":
                passing = record.artifact_id.inventory_consent in ("full", "limited")
                levels = criterion.level_ids.filtered(
                    lambda r, passing=passing: r.is_fail != passing
                ).sorted(lambda r: (r.sequence, r.id))
                result = levels[:1]
            record.level_id = result

    @api.depends("level_id", "criterion_id.gate_source")
    def _compute_level_text(self):
        """Copy the name of the level of an aspect filled by the system.

        A manual aspect keeps the stored text, which the create and
        write of the row set at the moment the level is picked.
        """
        for record in self:
            result = record.level_text
            if record.criterion_id.gate_source == "inventory_consent":
                result = record.level_id.name or False
            record.level_text = result

    @api.depends("level_id")
    def _compute_score(self):
        """Copy the score of the picked level.

        Only ``level_id`` triggers it, so a later edit of the score of
        the level does not move a given answer.
        """
        for record in self:
            result = 0
            if record.level_id:
                result = record.level_id.score
            record.score = result

    @api.constrains("level_id", "criterion_id")
    def _check_level_criterion(self):
        """Keep the picked level inside the levels of its aspect.

        :raises ValidationError: when the level belongs to another
            aspect
        """
        for record in self:
            level = record.level_id
            if level and level.criterion_id != record.criterion_id:
                raise ValidationError(
                    _(
                        """
Context: Assess learning artifact
Database ID: %s
Problem: The level does not belong to aspect %s
Solution: Pick a level of the aspect
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )

    def _check_manual_level(self):
        """Reject picking a level of an aspect filled from the consent.

        :raises UserError: when a row belongs to an aspect whose level
            comes from the inventory consent
        """
        for record in self:
            if record.criterion_id.gate_source == "inventory_consent":
                raise UserError(
                    _(
                        """
Context: Assess learning artifact
Database ID: %s
Problem: Aspect %s is filled automatically from the inventory consent
Solution: Change the consent of the students instead of picking a level
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )

    def _check_assessor(self):
        """Reject assessing by a user outside the groups of the aspect.

        Nothing is checked for the superuser or for an aspect that
        lists no group.

        :raises UserError: when the active user may not assess a row
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
Context: Assess learning artifact
Database ID: %s
Problem: You are not allowed to assess aspect %s
Solution: Ask a user in the assessor groups of the aspect to assess it
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )

    def _check_ethics_lock(self):
        """Reject picking a level of a scored aspect before the gate passes.

        :raises UserError: when the artifact has not passed the ethics
            gate and the row belongs to a scored aspect
        """
        for record in self:
            if (
                record.aspect_type == "score"
                and record.artifact_id.sudo().ethics_result != "pass"
            ):
                raise UserError(
                    _(
                        """
Context: Assess learning artifact
Database ID: %s
Problem: The ethics gate has not passed yet, so aspect %s is locked
Solution: Answer every ethics gate aspect with a passing level first
"""
                    )
                    % (record.id, record.criterion_id.display_name)
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Create rows and record who picked the level.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        obj_level = self.env["school_learning_artifact_rubric_criterion_level"]
        for vals in vals_list:
            if vals.get("level_id"):
                vals["level_text"] = obj_level.browse(vals["level_id"]).name
                vals["assessor_id"] = self.env.uid
                vals["date_score"] = fields.Datetime.now()
        records = super().create(vals_list)
        picked = self.browse()
        for record, vals in zip(records, vals_list):
            if vals.get("level_id"):
                picked |= record
        picked._check_manual_level()
        picked._check_assessor()
        picked._check_ethics_lock()
        # Compute the score now: it must be taken from the level as it is
        # at this moment, not at a later flush after the level was edited.
        picked.sudo().read(["score"])
        return records

    def write(self, vals):
        """Write rows and record who picked the level.

        :param vals: values to write
        :return: True
        """
        if "level_id" in vals:
            self._check_manual_level()
            self._check_assessor()
            if vals["level_id"]:
                self._check_ethics_lock()
                level = self.env[
                    "school_learning_artifact_rubric_criterion_level"
                ].browse(vals["level_id"])
                vals = dict(
                    vals,
                    level_text=level.name,
                    assessor_id=self.env.uid,
                    date_score=fields.Datetime.now(),
                )
            else:
                vals = dict(
                    vals,
                    level_text=False,
                    assessor_id=False,
                    date_score=False,
                )
        result = super().write(vals)
        if vals.get("level_id"):
            # Compute the score now, before the level can be edited.
            self.sudo().read(["score"])
        return result
