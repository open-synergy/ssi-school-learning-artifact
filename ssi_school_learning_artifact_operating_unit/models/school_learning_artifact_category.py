# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolLearningArtifactCategory(
    models.Model
):  # pylint: disable=too-few-public-methods
    _name = "school_learning_artifact_category"
    _inherit = [
        "school_learning_artifact_category",
        "mixin.multiple_operating_unit",
    ]

    # Adds the operating units that limit the visibility of the record.
