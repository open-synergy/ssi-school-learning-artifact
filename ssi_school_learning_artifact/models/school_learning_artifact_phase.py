# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactPhase(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a learning phase that a learning artifact can
    cover. Whether a school requires a phase is decided by the
    configuration of the school. The restriction per school is
    given by extension modules. The phase can also be limited to
    grade types and/or grades: an artifact then only offers the
    phases that match the grade type and the grade of its class.
    """

    _name = "school_learning_artifact_phase"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Phase"

    grade_type_ids = fields.Many2many(
        string="Grade Types",
        comodel_name="school_grade_type",
        help=(
            "The grade types this phase applies to. Leave empty to "
            "apply to every grade type. When grades are also filled "
            "in, the artifact must match both."
        ),
    )
    grade_ids = fields.Many2many(
        string="Grades",
        comodel_name="school_grade",
        help=(
            "The grades this phase applies to. Leave empty to apply "
            "to every grade. When grade types are also filled in, "
            "the artifact must match both."
        ),
    )
