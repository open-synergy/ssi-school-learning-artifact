# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class School(models.Model):  # pylint: disable=too-few-public-methods
    _name = "school"
    _inherit = ["school"]

    learning_artifact_link_prefix = fields.Char(
        string="Learning Artifact Link Prefix",
        help=(
            "Required beginning of the link of a learning artifact "
            "of this school, for example the URL of a shared folder. "
            "Leave empty to accept any link."
        ),
    )
    learning_artifact_require_component = fields.Boolean(
        string="Learning Artifact Requires Component",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a primary component before it can be submitted."
        ),
    )
    learning_artifact_require_dimension = fields.Boolean(
        string="Learning Artifact Requires Dimension",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a dimension before it can be submitted."
        ),
    )
    learning_artifact_require_phase = fields.Boolean(
        string="Learning Artifact Requires Phase",
        default=False,
        help=(
            "If checked, a learning artifact of this school must have "
            "a phase before it can be submitted."
        ),
    )
    learning_artifact_require_inventory_consent = fields.Boolean(
        string="Learning Artifact Requires Inventory Consent",
        default=False,
        help=(
            "If checked, a learning artifact of this school cannot be "
            "submitted while a student has no inventory consent recorded. "
            "A student who refused the inventory consent always blocks "
            "the submission."
        ),
    )
    showcase_min_publication_consent = fields.Selection(
        string="Showcase Minimum Publication Consent",
        selection=[
            ("full", "Full"),
            ("limited", "Limited"),
        ],
        default="full",
        required=True,
        help=(
            "Lowest aggregate publication consent of the students that "
            "lets an artifact of this school into the showcase. With "
            "Full, an artifact with a limited consent needs the "
            "treatment below."
        ),
    )
    showcase_limited_treatment = fields.Selection(
        string="Showcase Limited Consent Treatment",
        selection=[
            ("block", "Block"),
            ("review", "Review Task"),
        ],
        default="block",
        required=True,
        help=(
            "What happens to an artifact with a limited publication "
            "consent. Block keeps it out of the showcase. Review Task "
            "lets it in after a reviewer marked the consent as "
            "reviewed."
        ),
    )
    showcase_exclude_refused_member = fields.Boolean(
        string="Showcase Ignores Refusing Students",
        default=False,
        help=(
            "If checked, the students who refused the publication are "
            "left out when the publication consent of an artifact is "
            "checked for the showcase, as long as one student remains. "
            "They must then not be recognizable in the content."
        ),
    )
    showcase_consent_reviewer_group_id = fields.Many2one(
        string="Showcase Consent Reviewer Group",
        comodel_name="res.groups",
        ondelete="restrict",
        help=(
            "Group whose users can mark a limited publication consent "
            "as reviewed. Leave empty to let anyone who may edit the "
            "artifact do it."
        ),
    )
    showcase_narrative_max_revision = fields.Integer(
        string="Showcase Narrative Revision Limit",
        default=1,
        required=True,
        help=(
            "How many times the coordinator can return a showcase "
            "narrative to the teacher for a revision. Beyond the "
            "limit the coordinator revises the narrative."
        ),
    )

    @api.constrains("showcase_narrative_max_revision")
    def _check_showcase_narrative_max_revision(self):
        """Reject a negative revision limit.

        :raises ValidationError: when the limit is below 0
        """
        for record in self:
            if record.showcase_narrative_max_revision < 0:
                error_message = (
                    _(
                        """
Context: Check school
Database ID: %s
Problem: Showcase Narrative Revision Limit is negative
Solution: Set a limit of 0 or more
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
