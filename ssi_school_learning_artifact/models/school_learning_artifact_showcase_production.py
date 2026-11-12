# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator

from .school_learning_artifact import _SHOWCASE_CONSENT_DEPENDS

_COORDINATOR_GROUP = (
    "ssi_school_learning_artifact."
    "school_learning_artifact_inventory_coordinator_group"
)

# Narrative states in which the content is locked for everybody.
_CONTENT_LOCKED_STATES = ("submitted", "confirm", "approved")

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

    The narrative goes through a workflow. The inventory coordinator
    returns it to the teacher who made the artifact, the teacher
    writes it within the word limits of the channel and submits it,
    and the coordinator reviews it: it is returned for a revision
    (limited per school) or sent to the multiple approval. Only an
    approved narrative can be ready.
    """

    _name = "school_learning_artifact_showcase_production"
    _inherit = [
        "mail.thread",
        "mixin.policy",
        "mixin.multiple_approval",
    ]
    _description = "School Learning Artifact Showcase Production"
    _order = "artifact_id, id"

    _approval_from_state = "submitted"
    _approval_state = "confirm"
    _approval_to_state = "approved"
    _approval_reject_state = "reject"
    _approval_cancel_state = "draft"
    _after_approved_method = "_finish_narrative_approval"
    _automatically_insert_multiple_approval_page = False

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
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("assigned", "Assigned"),
            ("submitted", "Submitted"),
            ("confirm", "Waiting Approval"),
            ("approved", "Approved"),
            ("reject", "Rejected"),
        ],
        default="draft",
        required=True,
        readonly=True,
        copy=False,
        help=(
            "Status of the narrative. Draft is not written yet, "
            "Assigned is with the person in charge, Submitted waits "
            "for the review of the coordinator, Waiting Approval is "
            "in the approval and Approved can be ready. A Rejected "
            "narrative goes back to the writer."
        ),
    )
    narrative_revision_count = fields.Integer(
        string="Revision Count",
        default=0,
        readonly=True,
        copy=False,
        help=(
            "Number of times the narrative was returned to the "
            "teacher for a revision. Beyond the limit of the school "
            "the coordinator revises it."
        ),
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Approve policy

* If active user can see and execute 'Approve' button""",
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Reject policy

* If active user can see and execute 'Reject' button""",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
        compute_sudo=True,
        help="""Restart approval policy

* If active user can see and execute 'Restart Approval' button""",
    )
    content = fields.Text(
        string="Content",
        help=(
            "The text produced for the channel. It is locked once "
            "the narrative is submitted."
        ),
    )
    content_word_count = fields.Integer(
        string="Word Count",
        compute="_compute_content_word_count",
        compute_sudo=True,
        help=(
            "Number of words in the content. The narrative cannot be "
            "submitted outside the word limits of the channel."
        ),
    )
    pic_id = fields.Many2one(
        string="Person in Charge",
        comodel_name="res.users",
        ondelete="restrict",
        help=(
            "The user in charge of producing this content. It is the "
            "teacher of the artifact while the narrative is assigned."
        ),
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
            "Check when the content is ready to be distributed. Only an "
            "approved narrative can be ready. It is unchecked by "
            "itself when the publication consent of the artifact no "
            "longer meets the channel."
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
        The content is checked before it is written, see
        ``_check_content_editable``.

        :param vals: values to write
        :return: True
        :raises UserError: when the consent does not meet the channel
            or when the content may not be edited
        """
        if "content" in vals:
            self._check_content_editable(vals["content"])
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

    @api.constrains("ready", "state")
    def _check_ready_state(self):
        """Allow only an approved narrative to be ready.

        :raises ValidationError: when a production is ready but its
            narrative is not approved
        """
        for record in self:
            if record.ready and record.state != "approved":
                error_message = (
                    _(
                        """
Context: Check showcase production of learning artifact
Database ID: %s
Problem: Only an approved narrative can be ready
Solution: Get the narrative approved before checking Ready
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.model
    def _get_policy_field(self):
        """Return the policy boolean fields of the production.

        Extends the base list with the fields that control the
        Approve, Reject and Restart Approval buttons.

        :return: list of policy field names
        :rtype: list
        """
        res = super()._get_policy_field()
        res += [
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
        ]
        return res

    def _raise_narrative_error(self, context, problem, solution):
        """Raise the standard error of the narrative workflow.

        :param context: what the user was doing, already translated
        :param problem: what is wrong, already translated
        :param solution: how to fix it, already translated
        :raises UserError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: %s
Database ID: %s
Problem: %s
Solution: %s
"""
            )
            % (context, self.id, problem, solution)
        )
        raise UserError(error_message)

    def _is_coordinator(self):
        """Tell whether the active user is an inventory coordinator.

        The superuser always counts as a coordinator.

        :return: True when the active user may act as the coordinator
        :rtype: bool
        """
        user = self.env.user
        return self.env.uid == SUPERUSER_ID or user.has_group(_COORDINATOR_GROUP)

    def _check_coordinator(self, context):
        """Reject the users who are not an inventory coordinator.

        :param context: what the user is doing, already translated
        :raises UserError: when the active user is not a coordinator
        """
        self.ensure_one()
        if not self._is_coordinator():
            self._raise_narrative_error(
                context,
                _("You are not an inventory coordinator"),
                _("Ask a user in the Learning Artifact Inventory Coordinator group"),
            )

    def _check_narrative_state(self, context, states):
        """Reject a narrative that is not in one of the given states.

        :param context: what the user is doing, already translated
        :param states: tuple of the allowed states
        :raises UserError: when the state is not allowed
        """
        self.ensure_one()
        if self.state not in states:
            self._raise_narrative_error(
                context,
                _("The narrative is in status %s") % self.state,
                _("Use this action only in the status where it is shown"),
            )

    def _check_content_editable(self, content):
        """Reject a content change the workflow does not allow.

        The content is locked once the narrative is submitted. While
        it is assigned only the person in charge and the coordinator
        may change it. The superuser is never rejected.

        :param content: the new content
        :raises UserError: when the active user may not change it
        """
        if self.env.uid == SUPERUSER_ID:
            return
        for record in self:
            if (record.content or "") == (content or ""):
                continue
            context = _("Edit showcase production of learning artifact")
            if record.state in _CONTENT_LOCKED_STATES:
                record._raise_narrative_error(
                    context,
                    _("The content is locked in status %s") % record.state,
                    _("Ask the coordinator to return the narrative first"),
                )
            if (
                record.state == "assigned"
                and self.env.user != record.pic_id
                and not record._is_coordinator()
            ):
                record._raise_narrative_error(
                    context,
                    _("The narrative is assigned to %s") % record.pic_id.display_name,
                    _("Only the person in charge or a coordinator can edit it"),
                )

    def _schedule_narrative_activity(self):
        """Give the person in charge a To-Do on the artifact.

        The summary names the channel of the narrative.
        """
        self.ensure_one()
        self.artifact_id.sudo().activity_schedule(
            "mail.mail_activity_data_todo",
            user_id=self.pic_id.id,
            summary=_("Write the showcase narrative for channel %s")
            % self.channel_id.display_name,
        )

    def _ensure_policy_template(self):
        """Give a production created before the workflow its policy.

        Productions created before the policy template existed have no
        template, so none of their policy fields would be True.
        """
        for record in self.filtered(lambda r: not r.policy_template_id):
            record.action_reload_policy_template()

    def action_assign_to_teacher(self):
        """Return a draft narrative to the teacher of the artifact.

        Only a coordinator, only for a curated artifact. The person in
        charge becomes the teacher and receives a To-Do on the
        artifact.

        :raises UserError: when the user is not a coordinator, the
            narrative is not a draft or the artifact is not curated
        """
        context = _("Return showcase narrative to teacher")
        for record in self:
            record._check_coordinator(context)
            record._check_narrative_state(context, ("draft",))
            artifact = record.artifact_id
            if artifact.state != "done":
                record._raise_narrative_error(
                    context,
                    _("The artifact %s is not curated yet") % artifact.display_name,
                    _("Curate the artifact before returning its narrative"),
                )
            record.write(
                {
                    "state": "assigned",
                    "pic_id": artifact.user_id.id,
                    "ready": False,
                }
            )
            record._schedule_narrative_activity()

    def action_submit_narrative(self):
        """Submit an assigned narrative to the coordinator.

        The person in charge or a coordinator can submit it. The word
        count must be within the limits of the channel, a limit of 0
        means no limit.

        :raises UserError: when the user may not submit, or the word
            count is outside the limits of the channel
        """
        context = _("Submit showcase narrative")
        for record in self:
            record._check_narrative_state(context, ("assigned",))
            if self.env.uid != SUPERUSER_ID and not (
                self.env.user == record.pic_id or record._is_coordinator()
            ):
                record._raise_narrative_error(
                    context,
                    _("The narrative is assigned to %s") % record.pic_id.display_name,
                    _("Only the person in charge or a coordinator can submit it"),
                )
            count = record.content_word_count
            channel = record.channel_id
            if channel.min_words > 0 and count < channel.min_words:
                record._raise_narrative_error(
                    context,
                    _("The content has %s words, below the minimum of %s")
                    % (count, channel.min_words),
                    _("Write at least %s words") % channel.min_words,
                )
            if channel.max_words > 0 and count > channel.max_words:
                record._raise_narrative_error(
                    context,
                    _("The content has %s words, above the maximum of %s")
                    % (count, channel.max_words),
                    _("Shorten the content to %s words") % channel.max_words,
                )
            record.write({"state": "submitted"})

    def action_request_narrative_approval(self):
        """Send a submitted narrative to the multiple approval.

        Only a coordinator. The state is written first and the
        approval is requested explicitly, because the mixin only
        requests it when the stored template is empty at write time.

        :raises UserError: when the user is not a coordinator or the
            narrative is not submitted
        """
        context = _("Request approval of showcase narrative")
        for record in self:
            record._check_coordinator(context)
            record._check_narrative_state(context, ("submitted",))
            record._ensure_policy_template()
            record.write({"state": "confirm"})
            record.action_request_approval()

    def action_return_narrative(self):
        """Return a submitted or rejected narrative for a revision.

        Only a coordinator. While the revision count is below the
        limit of the school the narrative goes back to the teacher
        with a new To-Do and the count grows. Beyond the limit the
        coordinator becomes the person in charge and revises it.

        :raises UserError: when the user is not a coordinator or the
            narrative cannot be returned
        """
        context = _("Return showcase narrative")
        for record in self:
            record._check_coordinator(context)
            record._check_narrative_state(context, ("submitted", "reject"))
            limit = record.artifact_id.school_id.showcase_narrative_max_revision
            if record.state == "reject":
                record.sudo().approval_ids.unlink()
            if record.narrative_revision_count < limit:
                record.write(
                    {
                        "state": "assigned",
                        "pic_id": record.artifact_id.user_id.id,
                        "narrative_revision_count": record.narrative_revision_count + 1,
                    }
                )
                record._schedule_narrative_activity()
            else:
                record.write({"state": "assigned", "pic_id": self.env.user.id})

    def _finish_narrative_approval(self):
        """Mark the narrative as approved.

        Called by the multiple approval mixin once every approver
        approved.
        """
        self.ensure_one()
        self.write({"state": "approved"})

    def _check_narrative_approver(self, context):
        """Reject the approval of a user who is not an active approver.

        :param context: what the user is doing, already translated
        :raises UserError: when no approver is configured or the
            active user is not among the active approvers
        """
        self.ensure_one()
        if not self.approval_ids:
            self._raise_narrative_error(
                context,
                _("No approver is configured for the showcase narrative"),
                _(
                    "Ask the administrator to add the approvers to the "
                    "approval template, then click Restart Approval"
                ),
            )
        if self.env.user not in self.active_approver_user_ids:
            self._raise_narrative_error(
                context,
                _("You are not an active approver of the narrative"),
                _("Wait for your turn in the approval sequence"),
            )

    @ssi_decorator.pre_approve_check()
    def _10_check_narrative_approver(self):
        """Block the approval when nobody is configured to give it.

        An empty approval template creates no approval, and the mixin
        would then approve with one click. Raising here keeps the
        narrative waiting until the administrator fills the template
        and a coordinator restarts the approval.

        :raises UserError: when no approver is configured or the
            active user is not an active approver
        """
        self._check_narrative_approver(_("Approve showcase narrative"))

    @ssi_decorator.pre_reject_check()
    def _10_check_narrative_rejecter(self):
        """Block the rejection by a user who is not an active approver.

        :raises UserError: when no approver is configured or the
            active user is not an active approver
        """
        self._check_narrative_approver(_("Reject showcase narrative"))
