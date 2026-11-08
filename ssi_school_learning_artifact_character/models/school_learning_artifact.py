# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_TAGGABLE_STATUSES = ("effective", "partial")


class SchoolLearningArtifact(models.Model):
    _name = "school_learning_artifact"
    _inherit = [
        "school_learning_artifact",
    ]

    # Adds the character tag of the artifact.
    primary_subconstruct_id = fields.Many2one(
        string="Dominant Character Tag",
        comodel_name="school_character_subconstruct",
        ondelete="restrict",
        domain="[('id', 'in', allowed_subconstruct_ids)]",
        help=(
            "The character sub-construct that dominates this artifact. "
            "It is a tag of the activity, not evidence of the "
            "character achievement of a student."
        ),
    )
    secondary_subconstruct_id = fields.Many2one(
        string="Secondary Character Tag",
        comodel_name="school_character_subconstruct",
        ondelete="restrict",
        domain="[('id', 'in', allowed_subconstruct_ids)]",
        help=(
            "An additional character sub-construct that appears in " "this artifact."
        ),
    )
    character_not_evident = fields.Boolean(
        string="Not Clearly Evident",
        help=(
            "Check when no character sub-construct is clearly evident "
            "in this artifact. The dominant tag must then stay empty."
        ),
    )
    allowed_subconstruct_ids = fields.Many2many(
        string="Allowed Character Tags",
        comodel_name="school_character_subconstruct",
        compute="_compute_allowed_subconstruct_ids",
        compute_sudo=True,
        help=(
            "Active sub-constructs that can be tagged. When the grade "
            "type of the artifact has indicator statuses, only the "
            "sub-constructs with an Effective or Partial indicator at "
            "that grade type are listed."
        ),
    )
    character_indicator_ids = fields.Many2many(
        string="Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_character_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        domain="[('id', 'in', allowed_indicator_ids)]",
        help=(
            "The character indicators that appear in this artifact. "
            "Each indicator belongs to the dominant or the secondary "
            "character tag. It is a mark of the activity, not "
            "evidence of the character achievement of a student."
        ),
    )
    allowed_indicator_ids = fields.Many2many(
        string="Allowed Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_allowed_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        compute="_compute_allowed_indicator_ids",
        compute_sudo=True,
        help=(
            "Active indicators of an active sub-construct that can be "
            "selected. When a status line applies to the grade of the "
            "artifact, only the indicators that are Effective or "
            "Partial on those lines are listed."
        ),
    )
    character_tag_ok = fields.Boolean(
        string="Can Tag Character",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the character tags of this "
            "artifact can be filled in."
        ),
    )

    character_indicator_ok = fields.Boolean(
        string="Can Select Character Indicator",
        compute="_compute_policy",
        store=False,
        compute_sudo=True,
        help=(
            "Policy that determines whether the character indicators "
            "of this artifact can be selected."
        ),
    )

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        res.append("character_tag_ok")
        res.append("character_indicator_ok")
        return res

    @api.depends("grade_type_id", "grade_id")
    def _compute_allowed_subconstruct_ids(self):
        """List the character sub-constructs usable for the artifact.

        Every active sub-construct is usable. When the grade type of
        the artifact has at least one indicator status line, the
        choice is narrowed to the sub-constructs of the indicators
        that are Effective or Partial at that grade type.
        """
        obj_subconstruct = self.env["school_character_subconstruct"]
        obj_status = self.env["school_character_indicator_grade_status"]
        for record in self:
            result = obj_subconstruct.search(
                record._get_allowed_subconstruct_criteria()
            )
            statuses = obj_status.search(record._get_grade_status_criteria())
            if statuses:
                taggable = statuses.filtered(
                    lambda status: status.status in _TAGGABLE_STATUSES
                ).mapped("indicator_id.subconstruct_id")
                result = result & taggable
            record.allowed_subconstruct_ids = result

    def _get_allowed_subconstruct_criteria(self):
        """Build the search domain for the usable sub-constructs.

        Extension point: override to widen or narrow the choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [("active", "=", True)]

    def _get_grade_status_criteria(self):
        """Build the search domain for the indicator statuses.

        The statuses that count are the lines of the grade type of the
        artifact that have no grade or that include the grade of the
        artifact. An artifact without a grade type matches no line.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("grade_type_id", "=", self.grade_type_id.id),
            "|",
            ("grade_ids", "=", False),
            ("grade_ids", "in", self.grade_id.ids),
        ]

    @api.depends("grade_type_id", "grade_id")
    def _compute_allowed_indicator_ids(self):
        """List the character indicators usable for the artifact.

        Every active indicator of an active sub-construct is usable.
        When a status line applies to the grade of the artifact, the
        choice is narrowed to the indicators that are Effective or
        Partial on those lines.
        """
        obj_indicator = self.env["school_character_indicator"]
        obj_status = self.env["school_character_indicator_grade_status"]
        for record in self:
            result = obj_indicator.search(record._get_allowed_indicator_criteria())
            statuses = obj_status.search(record._get_grade_status_criteria())
            if statuses:
                taggable = statuses.filtered(
                    lambda status: status.status in _TAGGABLE_STATUSES
                ).mapped("indicator_id")
                result = result & taggable
            record.allowed_indicator_ids = result

    def _get_allowed_indicator_criteria(self):
        """Build the search domain for the usable indicators.

        Extension point: override to widen or narrow the choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("active", "=", True),
            ("subconstruct_id.active", "=", True),
        ]

    @api.constrains("character_not_evident", "primary_subconstruct_id")
    def _check_character_not_evident(self):
        """Forbid a dominant tag on an artifact marked as not evident.

        :raises ValidationError: when the artifact is marked as not
            clearly evident and still has a dominant tag.
        :return: None
        """
        for record in self:
            if record.character_not_evident and record.primary_subconstruct_id:
                error_message = (
                    _(
                        """
Context: Save learning artifact character tag
Database ID: %s
Problem: Dominant character tag is filled in while the artifact is marked as not clearly evident
Solution: Clear the dominant character tag or uncheck Not Clearly Evident
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains(
        "character_indicator_ids",
        "primary_subconstruct_id",
        "secondary_subconstruct_id",
        "character_not_evident",
    )
    def _check_character_indicator(self):
        """Ensure the indicators agree with the character tags.

        When a dominant or a secondary tag is filled in, the
        sub-construct of every selected indicator must be one of them.
        An artifact marked as not clearly evident has no indicator.

        :raises ValidationError: when an indicator does not belong to
            the tags or the artifact is marked as not clearly evident.
        :return: None
        """
        for record in self:
            if not record.character_indicator_ids:
                continue
            problem = False
            if record.character_not_evident:
                problem = _(
                    "Character indicator is selected while the artifact "
                    "is marked as not clearly evident"
                )
                solution = _(
                    "Clear the character indicators or uncheck Not Clearly " "Evident"
                )
            else:
                tags = record.primary_subconstruct_id | record.secondary_subconstruct_id
                if tags and (
                    record.character_indicator_ids.mapped("subconstruct_id") - tags
                    or record.character_indicator_ids.filtered(
                        lambda indicator: not indicator.subconstruct_id
                    )
                ):
                    problem = _(
                        "Character indicator does not belong to the "
                        "dominant or the secondary character tag"
                    )
                    solution = _(
                        "Select only indicators of the dominant or the "
                        "secondary character tag"
                    )
            if problem:
                error_message = (
                    _(
                        """
Context: Save learning artifact character indicator
Database ID: %s
Problem: %s
Solution: %s
"""
                    )
                    % (record.id, problem, solution)
                )
                raise ValidationError(error_message)
