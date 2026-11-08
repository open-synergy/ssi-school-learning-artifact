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
    Effective or Partial at the grade type of the artifact. A line can
    optionally be limited to some grades of the grade type, so the
    status can differ between the grades of one grade type. An
    indicator has one line without grades per grade type, or several
    lines with grades that do not overlap.
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
    grade_ids = fields.Many2many(
        string="Grades",
        comodel_name="school_grade",
        relation="school_character_indicator_grade_status_grade_rel",
        column1="status_id",
        column2="grade_id",
        domain="[('type_id', '=', grade_type_id)]",
        help=(
            "The grades of the grade type at which the indicator has "
            "this status. Leave empty to apply the status to every "
            "grade of the grade type."
        ),
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

    @api.constrains("indicator_id", "grade_type_id", "grade_ids")
    def _check_unique_grade_type(self):
        """Ensure the status lines of an indicator never overlap.

        For one indicator and one grade type there is either a single
        line without grades, or several lines whose grades do not
        overlap. Mixing a line without grades with a line with grades
        is rejected.

        :raises ValidationError: when another line of the same
            indicator and grade type overlaps this line.
        :return: None
        """
        for record in self:
            others = self.search(
                [
                    ("id", "!=", record.id),
                    ("indicator_id", "=", record.indicator_id.id),
                    ("grade_type_id", "=", record.grade_type_id.id),
                ]
            )
            for other in others:
                problem = record._get_overlap_problem(other)
                if problem:
                    error_message = (
                        _(
                            """
Context: Save character indicator grade status
Database ID: %s
Problem: %s
Solution: %s
"""
                        )
                        % (record.id, problem[0], problem[1])
                    )
                    raise ValidationError(error_message)

    def _get_overlap_problem(self, other):
        """Compare this line with another line of the same pair.

        :param other: another status line of the same indicator and
            grade type
        :return: tuple of problem and solution text, or False when the
            two lines do not overlap
        """
        self.ensure_one()
        if not self.grade_ids and not other.grade_ids:
            return (
                _("Indicator already has a status for this grade type"),
                _("Keep one status line per grade type for each indicator"),
            )
        if not self.grade_ids or not other.grade_ids:
            return (
                _(
                    "Indicator has a status line without grades and "
                    "a status line with grades for this grade type"
                ),
                _("Fill in the grades on every line or leave them empty"),
            )
        if self.grade_ids & other.grade_ids:
            return (
                _("Indicator has two status lines for the same grade"),
                _("Remove the shared grade from one of the lines"),
            )
        return False
