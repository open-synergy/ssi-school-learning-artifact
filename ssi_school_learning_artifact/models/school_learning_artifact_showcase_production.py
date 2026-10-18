# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolLearningArtifactShowcaseProduction(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents the content produced for one channel of the showcase of
    a learning artifact. It records the text, the person in charge and
    whether the content is ready to be distributed. The distribution
    itself happens outside Odoo.
    """

    _name = "school_learning_artifact_showcase_production"
    _description = "School Learning Artifact Showcase Production"
    _order = "artifact_id, id"

    artifact_id = fields.Many2one(
        string="Learning Artifact",
        comodel_name="school_learning_artifact",
        required=True,
        ondelete="cascade",
        help="The learning artifact this content is produced for.",
    )
    channel_id = fields.Many2one(
        string="Channel",
        comodel_name="school_learning_artifact_showcase_channel",
        required=True,
        ondelete="restrict",
        help="The channel this content is produced for.",
    )
    content = fields.Text(
        string="Content",
        help="The text produced for the channel.",
    )
    content_word_count = fields.Integer(
        string="Word Count",
        compute="_compute_content_word_count",
        compute_sudo=True,
        help=(
            "Number of words in the content. Informative only, it "
            "never blocks the content."
        ),
    )
    pic_id = fields.Many2one(
        string="Person in Charge",
        comodel_name="res.users",
        ondelete="restrict",
        help="The user in charge of producing this content.",
    )
    ready = fields.Boolean(
        string="Ready",
        default=False,
        help="Check when the content is ready to be distributed.",
    )
    date_published = fields.Date(
        string="Date Published",
        help="The date the content was distributed outside Odoo.",
    )
    note = fields.Text(
        string="Note",
        help="Any remark about this content.",
    )

    @api.depends("content")
    def _compute_content_word_count(self):
        """Count the words of the content.

        Words are the whitespace separated chunks of ``content``.
        """
        for record in self:
            result = 0
            if record.content:
                result = len(record.content.split())
            record.content_word_count = result
