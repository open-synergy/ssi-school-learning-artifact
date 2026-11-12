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

    # Adds the character tags of the artifact.
    dominant_subconstruct_ids = fields.Many2many(
        string="Dominant Character Tags",
        comodel_name="school_character_subconstruct",
        relation="school_learning_artifact_dominant_subconstruct_rel",
        column1="artifact_id",
        column2="subconstruct_id",
        domain="[('id', 'in', allowed_subconstruct_ids)]",
        help=(
            "The character sub-constructs that dominate this artifact. "
            "It is a tag of the activity, not evidence of the "
            "character achievement of a student. There is no limit "
            "on the number of tags."
        ),
    )
    secondary_subconstruct_ids = fields.Many2many(
        string="Secondary Character Tags",
        comodel_name="school_character_subconstruct",
        relation="school_learning_artifact_secondary_subconstruct_rel",
        column1="artifact_id",
        column2="subconstruct_id",
        domain="[('id', 'in', allowed_subconstruct_ids)]",
        help=(
            "Additional character sub-constructs that appear in this "
            "artifact. A sub-construct cannot be both a dominant and a "
            "secondary tag. There is no limit on the number of tags."
        ),
    )
    character_not_evident = fields.Boolean(
        string="Not Clearly Evident",
        help=(
            "Check when no character sub-construct is clearly evident "
            "in this artifact. The character tags and indicators must "
            "then stay empty."
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
    dominant_indicator_ids = fields.Many2many(
        string="Dominant Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_dominant_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        domain="[('id', 'in', allowed_dominant_indicator_ids)]",
        help=(
            "The character indicators that appear in this artifact and "
            "belong to a dominant character tag. It is a mark of the "
            "activity, not evidence of the character achievement of a "
            "student."
        ),
    )
    secondary_indicator_ids = fields.Many2many(
        string="Secondary Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_secondary_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        domain="[('id', 'in', allowed_secondary_indicator_ids)]",
        help=(
            "The character indicators that appear in this artifact and "
            "belong to a secondary character tag. It is a mark of the "
            "activity, not evidence of the character achievement of a "
            "student."
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
    allowed_dominant_indicator_ids = fields.Many2many(
        string="Allowed Dominant Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_allowed_dominant_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        compute="_compute_allowed_dominant_indicator_ids",
        compute_sudo=True,
        help=(
            "Allowed character indicators that belong to a dominant "
            "character tag of the artifact."
        ),
    )
    allowed_secondary_indicator_ids = fields.Many2many(
        string="Allowed Secondary Character Indicators",
        comodel_name="school_character_indicator",
        relation="school_learning_artifact_allowed_secondary_indicator_rel",
        column1="artifact_id",
        column2="indicator_id",
        compute="_compute_allowed_secondary_indicator_ids",
        compute_sudo=True,
        help=(
            "Allowed character indicators that belong to a secondary "
            "character tag of the artifact."
        ),
    )
    dominant_subconstruct_codes = fields.Char(
        string="Dominant Character Tag Codes",
        compute="_compute_dominant_subconstruct_codes",
        compute_sudo=True,
        help="Codes of the dominant character tags, separated by commas.",
    )
    secondary_subconstruct_codes = fields.Char(
        string="Secondary Character Tag Codes",
        compute="_compute_secondary_subconstruct_codes",
        compute_sudo=True,
        help="Codes of the secondary character tags, separated by commas.",
    )
    dominant_indicator_codes = fields.Char(
        string="Dominant Character Indicator Codes",
        compute="_compute_dominant_indicator_codes",
        compute_sudo=True,
        help="Codes of the dominant character indicators, separated by commas.",
    )
    secondary_indicator_codes = fields.Char(
        string="Secondary Character Indicator Codes",
        compute="_compute_secondary_indicator_codes",
        compute_sudo=True,
        help="Codes of the secondary character indicators, separated by commas.",
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

    @api.depends(
        "grade_type_id",
        "grade_id",
        "dominant_subconstruct_ids",
        "allowed_indicator_ids",
    )
    def _compute_allowed_dominant_indicator_ids(self):
        """List the allowed indicators of the dominant character tags.

        The indicators are those of the usable indicators of the
        artifact whose sub-construct is a dominant character tag.
        """
        for record in self:
            record.allowed_dominant_indicator_ids = (
                record.allowed_indicator_ids.filtered(
                    lambda indicator, tags=record.dominant_subconstruct_ids: (
                        indicator.subconstruct_id in tags
                    )
                )
            )

    @api.depends(
        "grade_type_id",
        "grade_id",
        "secondary_subconstruct_ids",
        "allowed_indicator_ids",
    )
    def _compute_allowed_secondary_indicator_ids(self):
        """List the allowed indicators of the secondary character tags.

        The indicators are those of the usable indicators of the
        artifact whose sub-construct is a secondary character tag.
        """
        for record in self:
            record.allowed_secondary_indicator_ids = (
                record.allowed_indicator_ids.filtered(
                    lambda indicator, tags=record.secondary_subconstruct_ids: (
                        indicator.subconstruct_id in tags
                    )
                )
            )

    @api.depends("dominant_subconstruct_ids.code")
    def _compute_dominant_subconstruct_codes(self):
        """Join the codes of the dominant character tags."""
        for record in self:
            record.dominant_subconstruct_codes = ", ".join(
                record.dominant_subconstruct_ids.mapped("code")
            )

    @api.depends("secondary_subconstruct_ids.code")
    def _compute_secondary_subconstruct_codes(self):
        """Join the codes of the secondary character tags."""
        for record in self:
            record.secondary_subconstruct_codes = ", ".join(
                record.secondary_subconstruct_ids.mapped("code")
            )

    @api.depends("dominant_indicator_ids.code")
    def _compute_dominant_indicator_codes(self):
        """Join the codes of the dominant character indicators."""
        for record in self:
            record.dominant_indicator_codes = ", ".join(
                record.dominant_indicator_ids.mapped("code")
            )

    @api.depends("secondary_indicator_ids.code")
    def _compute_secondary_indicator_codes(self):
        """Join the codes of the secondary character indicators."""
        for record in self:
            record.secondary_indicator_codes = ", ".join(
                record.secondary_indicator_ids.mapped("code")
            )

    @api.onchange("character_not_evident")
    def onchange_dominant_subconstruct_ids(self):
        """Clear the dominant tags when marked as not clearly evident."""
        if self.character_not_evident:
            self.dominant_subconstruct_ids = [(5, 0, 0)]

    @api.onchange("character_not_evident")
    def onchange_secondary_subconstruct_ids(self):
        """Clear the secondary tags when marked as not clearly evident."""
        if self.character_not_evident:
            self.secondary_subconstruct_ids = [(5, 0, 0)]

    @api.onchange("character_not_evident")
    def onchange_dominant_indicator_ids(self):
        """Clear the dominant indicators when marked as not evident."""
        if self.character_not_evident:
            self.dominant_indicator_ids = [(5, 0, 0)]

    @api.onchange("character_not_evident")
    def onchange_secondary_indicator_ids(self):
        """Clear the secondary indicators when marked as not evident."""
        if self.character_not_evident:
            self.secondary_indicator_ids = [(5, 0, 0)]

    def _get_character_not_evident_clear_values(self):
        """Build the values that empty the character marks.

        Extension point: override to add the fields to be emptied
        when the artifact is marked as not clearly evident.

        :return: dictionary of values that clear the character marks
        """
        return {
            "dominant_subconstruct_ids": [(5, 0, 0)],
            "secondary_subconstruct_ids": [(5, 0, 0)],
            "dominant_indicator_ids": [(5, 0, 0)],
            "secondary_indicator_ids": [(5, 0, 0)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Create artifacts and empty the marks of unclear ones.

        When ``character_not_evident`` is checked in the values, the
        character tags and indicators are emptied, even when they are
        sent together.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        new_vals_list = []
        for vals in vals_list:
            if vals.get("character_not_evident"):
                vals = dict(vals)
                vals.update(self._get_character_not_evident_clear_values())
            new_vals_list.append(vals)
        return super().create(new_vals_list)

    def write(self, vals):
        """Write artifacts and empty the marks of unclear ones.

        When ``character_not_evident`` is checked in the values, the
        character tags and indicators are emptied, even when they are
        sent together.

        :param vals: values to write
        :return: True
        """
        if vals.get("character_not_evident"):
            vals = dict(vals)
            vals.update(self._get_character_not_evident_clear_values())
        return super().write(vals)

    @api.constrains("dominant_subconstruct_ids", "secondary_subconstruct_ids")
    def _check_character_tag_overlap(self):
        """Forbid a sub-construct that is both dominant and secondary.

        :raises ValidationError: when a sub-construct is in both the
            dominant and the secondary character tags.
        :return: None
        """
        for record in self:
            overlap = (
                record.dominant_subconstruct_ids & record.secondary_subconstruct_ids
            )
            if overlap:
                error_message = (
                    _(
                        """
Context: Save learning artifact character tag
Database ID: %s
Problem: Character tag is both dominant and secondary: %s
Solution: Keep the character tag in the dominant or in the secondary tags only
"""
                    )
                    % (record.id, ", ".join(overlap.mapped("display_name")))
                )
                raise ValidationError(error_message)

    @api.constrains("character_not_evident", "dominant_subconstruct_ids")
    def _check_character_not_evident(self):
        """Forbid a dominant tag on an artifact marked as not evident.

        :raises ValidationError: when the artifact is marked as not
            clearly evident and still has a dominant tag.
        :return: None
        """
        for record in self:
            if record.character_not_evident and record.dominant_subconstruct_ids:
                error_message = (
                    _(
                        """
Context: Save learning artifact character tag
Database ID: %s
Problem: Dominant character tag is filled in while the artifact is marked as not clearly evident
Solution: Clear the dominant character tags or uncheck Not Clearly Evident
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains(
        "dominant_indicator_ids",
        "secondary_indicator_ids",
        "dominant_subconstruct_ids",
        "secondary_subconstruct_ids",
        "character_not_evident",
    )
    def _check_character_indicator(self):
        """Ensure the indicators agree with the character tags.

        The sub-construct of every dominant indicator must be a
        dominant tag and the sub-construct of every secondary
        indicator must be a secondary tag. An indicator without a
        sub-construct is rejected. An artifact marked as not clearly
        evident has no indicator.

        :raises ValidationError: when an indicator does not belong to
            the tags or the artifact is marked as not clearly evident.
        :return: None
        """
        for record in self:
            indicators = record.dominant_indicator_ids | record.secondary_indicator_ids
            if not indicators:
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
            elif record.dominant_indicator_ids.filtered(
                lambda indicator, tags=record.dominant_subconstruct_ids: (
                    indicator.subconstruct_id not in tags
                )
            ) or record.secondary_indicator_ids.filtered(
                lambda indicator, tags=record.secondary_subconstruct_ids: (
                    indicator.subconstruct_id not in tags
                )
            ):
                problem = _(
                    "Character indicator does not belong to the "
                    "dominant or the secondary character tags"
                )
                solution = _(
                    "Select only dominant indicators of the dominant "
                    "tags and secondary indicators of the secondary tags"
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
