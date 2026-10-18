# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactEthicsReason(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a reason that a curator can pick when a learning
    artifact fails the ethics gate. A reason can be limited to some
    schools or left open to every school.
    """

    _name = "school_learning_artifact_ethics_reason"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Ethics Reason"

    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        relation="school_la_ethics_reason_school_rel",
        column1="reason_id",
        column2="school_id",
        help=(
            "Schools that can use this reason. Leave empty to make "
            "the reason available to every school."
        ),
    )
