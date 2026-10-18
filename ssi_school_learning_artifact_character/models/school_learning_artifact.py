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

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        res.append("character_tag_ok")
        return res

    @api.depends("grade_type_id")
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
        artifact. An artifact without a grade type matches no line.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [("grade_type_id", "=", self.grade_type_id.id)]

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
