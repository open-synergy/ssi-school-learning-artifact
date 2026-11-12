# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactCurationStatus(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a curation status that the rubric of a school can give
    to a learning artifact. The category is fixed and read by other
    modules, while the name is the label each school shows to its
    users. The restriction per school is given by extension
    modules.
    """

    _name = "school_learning_artifact_curation_status"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Curation Status"

    category = fields.Selection(
        string="Category",
        selection=[
            ("eligible", "Eligible"),
            ("revision", "Needs Revision"),
            ("archive", "Archive"),
            ("rejected", "Not Eligible"),
        ],
        required=True,
        help=(
            "Meaning of the status for the workflow. Eligible means the "
            "artifact passed the curation, Needs Revision allows it to "
            "be reopened, Archive keeps it out of use and Not Eligible "
            "archives it with the reason of the curator."
        ),
    )
