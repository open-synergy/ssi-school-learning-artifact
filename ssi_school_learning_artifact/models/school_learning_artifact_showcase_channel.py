# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolLearningArtifactShowcaseChannel(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a channel through which a curated learning artifact is
    showcased. The module only records the planning and the production
    per channel, the distribution itself happens outside Odoo. The
    restriction per school is given by extension modules. A channel
    can also require a full publication consent of the artifact
    before a production can be recorded for it.
    """

    _name = "school_learning_artifact_showcase_channel"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Showcase Channel"

    min_publication_consent = fields.Selection(
        string="Minimum Publication Consent",
        selection=[
            ("full", "Full"),
            ("limited", "Limited"),
        ],
        default="limited",
        required=True,
        help=(
            "Publication consent that an artifact needs before a "
            "production can be recorded for this channel. Limited "
            "adds no requirement. Full accepts only the artifacts "
            "whose effective publication consent is full."
        ),
    )
    content_guideline = fields.Text(
        string="Content Guideline",
        help=(
            "Advice on the content for this channel, for example the "
            "tone of the text. The length is limited by the minimum "
            "and maximum words."
        ),
    )
    min_words = fields.Integer(
        string="Minimum Words",
        default=0,
        help=(
            "Fewest words a narrative for this channel needs before "
            "it can be submitted. 0 means no minimum."
        ),
    )
    max_words = fields.Integer(
        string="Maximum Words",
        default=0,
        help=(
            "Most words a narrative for this channel can have before "
            "it can be submitted. 0 means no maximum."
        ),
    )

    @api.constrains("min_words", "max_words")
    def _check_words_range(self):
        """Reject a minimum above the maximum.

        :raises ValidationError: when both limits are set and the
            minimum is above the maximum
        """
        for record in self:
            if record.min_words > 0 and record.max_words > 0:
                if record.min_words > record.max_words:
                    error_message = (
                        _(
                            """
Context: Check showcase channel
Database ID: %s
Problem: Minimum Words is above Maximum Words
Solution: Set a minimum that is not above the maximum
"""
                        )
                        % (record.id,)
                    )
                    raise ValidationError(error_message)
