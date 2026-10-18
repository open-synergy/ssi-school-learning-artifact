# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactCategory(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a category used to classify learning artifacts,
    for example a recognition or curation category. A category
    can be limited to some schools or left open to all schools.
    """

    _name = "school_learning_artifact_category"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Category"

    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        help=(
            "Schools that can use this category. Leave empty to make "
            "the category available to every school."
        ),
    )
