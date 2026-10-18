# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolCharacterIndicatorGradeStatus(models.Model):
    """
    Represents the status of one character indicator for one grade
    type, for example Effective, Partial or Not Effective at the
    primary level. A school that configures these statuses narrows the
    character sub-constructs that can be tagged on a learning artifact
    to the sub-constructs that have at least one indicator that is
    Effective or Partial at the grade type of the artifact. An
    indicator has at most one status per grade type.
    """

    _name = "school_character_indicator_grade_status"
    _description = "Character Indicator Grade Status"

    indicator_id = fields.Many2one(
        string="Indicator",
        comodel_name="school_character_indicator",
        required=True,
        ondelete="cascade",
        help="The character indicator that this status applies to.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        required=True,
        ondelete="restrict",
        help="The grade type at which the indicator has this status.",
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ("effective", "Effective"),
            ("partial", "Partial"),
            ("not_effective", "Not Effective"),
        ],
        required=True,
        help=(
            "How effective the indicator is at the grade type. Only an "
            "Effective or Partial indicator makes its sub-construct "
            "available for tagging a learning artifact."
        ),
    )

    @api.constrains("indicator_id", "grade_type_id")
    def _check_unique_grade_type(self):
        """Ensure an indicator has one status per grade type.

        :raises ValidationError: when another line of the same
            indicator already carries the same grade type.
        :return: None
        """
        for record in self:
            duplicate = self.search_count(
                [
                    ("id", "!=", record.id),
                    ("indicator_id", "=", record.indicator_id.id),
                    ("grade_type_id", "=", record.grade_type_id.id),
                ]
            )
            if duplicate:
                error_message = (
                    _(
                        """
Context: Save character indicator grade status
Database ID: %s
Problem: Indicator already has a status for this grade type
Solution: Keep one status line per grade type for each indicator
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
