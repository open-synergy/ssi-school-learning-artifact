# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactShowcaseChannel(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a channel through which a curated learning artifact is
    showcased. The module only records the planning and the production
    per channel, the distribution itself happens outside Odoo. A
    channel can be limited to some schools or left open to every
    school.
    """

    _name = "school_learning_artifact_showcase_channel"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Showcase Channel"

    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        relation="school_la_showcase_channel_school_rel",
        column1="channel_id",
        column2="school_id",
        help=(
            "Schools that can use this channel. Leave empty to make "
            "the channel available to every school."
        ),
    )
    content_guideline = fields.Text(
        string="Content Guideline",
        help=(
            "Advice on the content for this channel, for example the "
            "suggested length of the text. It never blocks the content."
        ),
    )
