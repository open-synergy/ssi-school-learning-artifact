# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from .school_learning_artifact import _SHOWCASE_CONSENT_DEPENDS

_CHANNEL_CONSENT_DEPENDS = ("channel_id.min_publication_consent",) + tuple(
    "artifact_id." + path for path in _SHOWCASE_CONSENT_DEPENDS
)


class SchoolLearningArtifactShowcaseProduction(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents the content produced for one channel of the showcase of
    a learning artifact. It records the text, the person in charge and
    whether the content is ready to be distributed. The distribution
    itself happens outside Odoo. A channel that needs a full
    publication consent refuses the artifacts without it.
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
    channel_consent_ok = fields.Boolean(
        string="Consent Meets Channel",
        compute="_compute_channel_consent_ok",
        store=True,
        compute_sudo=True,
        help=(
            "Checked when the publication consent of the artifact "
            "meets the minimum publication consent of the channel. "
            "It follows the consent: it is unchecked when the consent "
            "of a student is withdrawn or lowered."
        ),
    )
    ready = fields.Boolean(
        string="Ready",
        default=False,
        compute="_compute_ready",
        store=True,
        readonly=False,
        compute_sudo=True,
        help=(
            "Check when the content is ready to be distributed. It is "
            "unchecked by itself when the publication consent of the "
            "artifact no longer meets the channel."
        ),
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

    @api.depends(*_CHANNEL_CONSENT_DEPENDS)
    def _compute_channel_consent_ok(self):
        """Check the consent of the artifact against the channel.

        A channel that needs a full publication consent is met only
        when the effective publication consent of the artifact is
        full. Any other channel has no requirement.
        """
        for record in self:
            result = True
            if record.channel_id.min_publication_consent == "full":
                result = bool(
                    record.artifact_id
                    and record.artifact_id._get_showcase_publication_consent() == "full"
                )
            record.channel_consent_ok = result

    @api.depends("channel_consent_ok")
    def _compute_ready(self):
        """Uncheck ready when the consent no longer meets the channel.

        The stored value is kept as long as the consent meets the
        channel, so a user can still check or uncheck it by hand.
        """
        for record in self:
            result = record.ready
            if not record.channel_consent_ok:
                result = False
            record.ready = result

    @api.model_create_multi
    def create(self, vals_list):
        """Create the productions and check the consent of the channel.

        :param vals_list: list of values of the new productions
        :return: the new productions
        :raises UserError: when the consent does not meet the channel
        """
        records = super().create(vals_list)
        records._check_channel_consent()
        return records

    def write(self, vals):
        """Write the productions and check the consent of the channel.

        The check runs when the channel or the artifact changes, and
        when the production is set as ready. Editing the other fields
        of a production that no longer meets the channel stays allowed.

        :param vals: values to write
        :return: True
        :raises UserError: when the consent does not meet the channel
        """
        result = super().write(vals)
        if vals.get("channel_id") or vals.get("artifact_id") or vals.get("ready"):
            self._check_channel_consent()
        return result

    def _check_channel_consent(self):
        """Reject the productions whose consent does not meet the channel.

        :raises UserError: when a publication consent of the artifact
            does not meet the minimum of the channel
        """
        for record in self:
            if not record.channel_consent_ok:
                error_message = (
                    _(
                        """
Context: Record showcase production of learning artifact
Database ID: %s
Problem: Channel %s requires a full publication consent
Solution: Record a full publication consent for every student or pick another channel
"""
                    )
                    % (record.id, record.channel_id.display_name)
                )
                raise UserError(error_message)
