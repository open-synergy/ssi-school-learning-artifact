# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolLearningArtifactCategory(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a category used to classify learning artifacts,
    for example a recognition or curation category. The restriction
    per school is given by extension modules.
    """

    _name = "school_learning_artifact_category"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Category"
