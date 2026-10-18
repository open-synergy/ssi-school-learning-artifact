# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator

_DRAFT_EDITABLE = {
    "draft": [
        ("readonly", False),
    ],
}

_OPEN_EDITABLE = {
    "open": [
        ("readonly", False),
    ],
}

_CONSENT_SELECTION = [
    ("full", "Full"),
    ("limited", "Limited"),
    ("refused", "Refused"),
    ("unknown", "Not Recorded"),
]

# Usages of an artifact that a data privacy consent purpose can cover.
_CONSENT_USAGES = ("inventory", "assessment", "publication", "promotion")

# The strictest consent of the students wins, in this order.
_CONSENT_RANK = {
    "full": 0,
    "limited": 1,
    "unknown": 2,
    "refused": 3,
}

_CONSENT_DEPENDS = (
    "school_id",
    "student_ids",
    "student_ids.contact_id",
    "student_ids.contact_id.consent_ids",
    "student_ids.contact_id.consent_ids.school_id",
    "student_ids.contact_id.consent_ids.purpose_id",
    "student_ids.contact_id.consent_ids.purpose_id.learning_artifact_usage",
    "student_ids.contact_id.consent_ids.consent_type",
    "student_ids.contact_id.consent_ids.consent_level",
    "student_ids.contact_id.consent_ids.consent_date",
)

_SHOWCASE_CONSENT_DEPENDS = _CONSENT_DEPENDS + (
    "publication_consent",
    "assessment_consent",
    "consent_reviewed",
    "school_id.showcase_min_publication_consent",
    "school_id.showcase_limited_treatment",
    "school_id.showcase_exclude_refused_member",
)


class SchoolLearningArtifact(models.Model):
    """
    Represents one Learning Artifact: a photo, video or document that
    records a learning activity, project or achievement of one or more
    students. A teacher records the artifact (Draft), submits it for
    curation (Waiting for Approval), may withdraw it again with Restart
    while the curator has not started yet, and the curator starts the
    curation by approving it (On Progress). The curator then fills in
    the ethics gate and the scores of the rubric of the school, and
    finishes the curation (Curated). An artifact whose curation status
    asks for a revision can be reopened a limited number of times. The
    workflow is Draft -> Confirm -> Approve -> Open -> Done, plus
    Cancel from draft, confirm and reject. The parental consent of the
    students per usage is read from the data privacy consent log and
    shown as the strictest consent of the students; a refused
    inventory consent blocks the submission. A curated artifact is
    placed on the showcase board, an internal record of the selection,
    the production per channel and the distribution of the artifact,
    whose stages, channels and rules are configuration data; the
    showcase itself happens outside Odoo. Every school specific choice
    (areas, categories, dimensions, phases, distinctive programs,
    graduate profiles, link prefix and the required-field switches) is
    configuration data kept per school or per branch, never hard-coded
    in this module.
    """

    _name = "school_learning_artifact"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "School Learning Artifact"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    # Overloading: the done state is shown as Curated.
    state = fields.Selection(
        selection_add=[
            ("done", "Curated"),
        ],
    )
    # Overloading: the document number is shown as the artifact code.
    name = fields.Char(
        string="Code",
    )
    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The date the learning activity or achievement took place.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The school unit that owns this artifact. Its configuration "
            "decides which fields are required and which master data "
            "can be selected."
        ),
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        ondelete="restrict",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The academic year in which the activity took place.",
    )
    grade_class_id = fields.Many2one(
        string="Class",
        comodel_name="school_grade_class",
        required=True,
        ondelete="restrict",
        domain="[('school_id', '=', school_id)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The homeroom class of the students. Only classes of the "
            "selected school can be chosen."
        ),
    )
    grade_id = fields.Many2one(
        string="Grade",
        comodel_name="school_grade",
        related="grade_class_id.grade_id",
        store=True,
        compute_sudo=True,
        help="The grade level of the selected class, filled automatically.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        related="grade_class_id.grade_type_id",
        store=True,
        compute_sudo=True,
        help="The grade type of the selected class, filled automatically.",
    )
    student_ids = fields.Many2many(
        string="Students",
        comodel_name="school_student",
        domain="[('school_id', '=', school_id)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The students featured in this artifact. At least one "
            "student is required before the artifact can be submitted."
        ),
    )
    learning_area_id = fields.Many2one(
        string="Learning Area",
        comodel_name="school_learning_artifact_area",
        ondelete="restrict",
        domain="[('school_id', '=', school_id)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The subject, activity area, development area or "
            "competition field of this artifact. Required before the "
            "artifact can be submitted."
        ),
    )
    activity_name = fields.Char(
        string="Activity Name",
        required=True,
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="Short title of the learning activity or achievement.",
    )
    activity_type = fields.Selection(
        string="Activity Type",
        selection=[
            ("intracurricular", "Intracurricular"),
            ("cocurricular", "Cocurricular"),
            ("extracurricular", "Extracurricular"),
        ],
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="Whether the activity is intra-, co- or extracurricular.",
    )
    primary_component_id = fields.Many2one(
        string="Primary Component",
        comodel_name="school_distinctive_program_component",
        ondelete="restrict",
        domain="[('id', 'in', allowed_component_ids)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The dominant component of the distinctive program that "
            "this artifact supports. Required when the school "
            "requires a component."
        ),
    )
    secondary_component_id = fields.Many2one(
        string="Secondary Component",
        comodel_name="school_distinctive_program_component",
        ondelete="restrict",
        domain="[('id', 'in', allowed_component_ids)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "An additional component of the distinctive program that "
            "this artifact supports."
        ),
    )
    dimension_id = fields.Many2one(
        string="Dimension",
        comodel_name="school_learning_artifact_dimension",
        ondelete="restrict",
        domain="[('id', 'in', allowed_dimension_ids)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The learning dimension covered by this artifact. "
            "Required when the school requires a dimension."
        ),
    )
    phase_id = fields.Many2one(
        string="Phase",
        comodel_name="school_learning_artifact_phase",
        ondelete="restrict",
        domain="[('id', 'in', allowed_phase_ids)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The learning phase covered by this artifact. Required "
            "when the school requires a phase."
        ),
    )
    graduate_profile_id = fields.Many2one(
        string="Graduate Profile",
        comodel_name="school_graduate_profile",
        compute="_compute_graduate_profile_id",
        store=True,
        compute_sudo=True,
        help=(
            "The first active graduate profile, by sequence, that "
            "covers the grade of the class. Filled automatically."
        ),
    )
    media_type = fields.Selection(
        string="Media Type",
        selection=[
            ("photo", "Photo"),
            ("video", "Video"),
            ("document", "Document"),
        ],
        required=True,
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The kind of media that documents the activity.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="school_learning_artifact_category",
        ondelete="restrict",
        domain="['|', ('school_ids', '=', False), ('school_ids', 'in', school_id)]",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "The category of this artifact. Required before the "
            "artifact can be submitted."
        ),
    )
    achievement_level = fields.Selection(
        string="Achievement Level",
        selection=[
            ("school", "School"),
            ("city", "City"),
            ("province", "Province"),
            ("national", "National"),
            ("international", "International"),
        ],
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The level at which an achievement was reached, if any.",
    )
    description = fields.Text(
        string="Description",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "Description of the media and the activity. Required "
            "before the artifact can be submitted."
        ),
    )
    description_word_count = fields.Integer(
        string="Word Count",
        compute="_compute_description_word_count",
        compute_sudo=True,
        help=(
            "Number of words in the description. Informative only, "
            "it never blocks the artifact."
        ),
    )
    link_url = fields.Char(
        string="Link",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help=(
            "Link to the media file. When the school defines a link "
            "prefix, the link must start with it."
        ),
    )
    activity_stage = fields.Selection(
        string="Activity Stage",
        selection=[
            ("beginning", "Beginning"),
            ("process", "Process"),
            ("end", "End"),
        ],
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The stage of the activity that the media captures.",
    )
    teacher_reflection = fields.Text(
        string="Teacher Reflection",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The teacher's reflection on the activity.",
    )
    student_reflection = fields.Text(
        string="Student Reflection",
        readonly=True,
        states=_DRAFT_EDITABLE,
        help="The students' reflection on the activity.",
    )
    rubric_id = fields.Many2one(
        string="Rubric",
        comodel_name="school_learning_artifact_rubric",
        compute="_compute_rubric_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        states=_DRAFT_EDITABLE,
        ondelete="restrict",
        help=(
            "The curation rubric of the artifact. It is the active "
            "rubric of the school, or the fallback rubric without "
            "schools when the school has none."
        ),
    )
    score_ids = fields.One2many(
        string="Scores",
        comodel_name="school_learning_artifact_score",
        inverse_name="artifact_id",
        readonly=True,
        states=_OPEN_EDITABLE,
        help="The scores of the aspects of the rubric.",
    )
    ethics_result = fields.Selection(
        string="Ethics Result",
        selection=[
            ("pass", "Pass"),
            ("fail", "Fail"),
        ],
        readonly=True,
        states=_OPEN_EDITABLE,
        help=(
            "Result of the ethics gate. It is required to finish the "
            "curation, and a failed gate gives the ethics fail status "
            "of the rubric."
        ),
    )
    ethics_reason_id = fields.Many2one(
        string="Ethics Reason",
        comodel_name="school_learning_artifact_ethics_reason",
        ondelete="restrict",
        domain="['|', ('school_ids', '=', False), ('school_ids', 'in', school_id)]",
        readonly=True,
        states=_OPEN_EDITABLE,
        help="The reason why the artifact failed the ethics gate.",
    )
    ethics_assessor_id = fields.Many2one(
        string="Ethics Assessor",
        comodel_name="res.users",
        readonly=True,
        help="The user who set the ethics result.",
    )
    total_score = fields.Integer(
        string="Total Score",
        compute="_compute_total_score",
        store=True,
        compute_sudo=True,
        help="The sum of the scores of all aspects.",
    )
    curation_status_id = fields.Many2one(
        string="Curation Status",
        comodel_name="school_learning_artifact_curation_status",
        compute="_compute_curation_status_id",
        store=True,
        compute_sudo=True,
        help=(
            "The curation status derived from the ethics result, the "
            "knockout aspects and the total score."
        ),
    )
    curation_status_category = fields.Selection(
        string="Curation Status Category",
        related="curation_status_id.category",
        store=True,
        compute_sudo=True,
        help="The category of the curation status.",
    )
    recommendation = fields.Text(
        string="Recommendation",
        readonly=True,
        states=_OPEN_EDITABLE,
        help=(
            "Advice of the curator to strengthen the artifact. "
            "Required when the status needs a revision."
        ),
    )
    curator_note = fields.Text(
        string="Curator Note",
        readonly=True,
        states=_OPEN_EDITABLE,
        help=(
            "Note of the curator. Required as the reason when the "
            "artifact is not eligible and is archived."
        ),
    )
    curated_by_id = fields.Many2one(
        string="Curated By",
        comodel_name="res.users",
        readonly=True,
        help="The user who finished the curation.",
    )
    date_curated = fields.Datetime(
        string="Curated On",
        readonly=True,
        help="The time the curation was finished.",
    )
    revision_count = fields.Integer(
        string="Revision Count",
        default=0,
        readonly=True,
        help="How many times the artifact was reopened for revision.",
    )
    allowed_component_ids = fields.Many2many(
        string="Allowed Components",
        comodel_name="school_distinctive_program_component",
        compute="_compute_allowed_component_ids",
        compute_sudo=True,
        help=(
            "Components of the distinctive programs configured for the "
            "branch of the selected school."
        ),
    )
    allowed_dimension_ids = fields.Many2many(
        string="Allowed Dimensions",
        comodel_name="school_learning_artifact_dimension",
        compute="_compute_allowed_dimension_ids",
        compute_sudo=True,
        help=(
            "Dimensions that apply to the selected school. A dimension "
            "without schools applies to every school."
        ),
    )
    allowed_phase_ids = fields.Many2many(
        string="Allowed Phases",
        comodel_name="school_learning_artifact_phase",
        compute="_compute_allowed_phase_ids",
        compute_sudo=True,
        help=(
            "Phases that apply to the selected school. A phase without "
            "schools applies to every school."
        ),
    )

    inventory_consent = fields.Selection(
        string="Inventory Consent",
        selection=_CONSENT_SELECTION,
        compute="_compute_consent",
        store=True,
        compute_sudo=True,
        help=(
            "The strictest parental consent of the students of this "
            "artifact to keep it in the inventory, of the school of the "
            "artifact."
        ),
    )
    assessment_consent = fields.Selection(
        string="Assessment Consent",
        selection=_CONSENT_SELECTION,
        compute="_compute_consent",
        store=True,
        compute_sudo=True,
        help=(
            "The strictest parental consent of the students of this "
            "artifact to assess it internally, of the school of the "
            "artifact."
        ),
    )
    publication_consent = fields.Selection(
        string="Publication Consent",
        selection=_CONSENT_SELECTION,
        compute="_compute_consent",
        store=True,
        compute_sudo=True,
        help=(
            "The strictest parental consent of the students of this "
            "artifact to publish it, of the school of the artifact."
        ),
    )
    promotion_consent = fields.Selection(
        string="Promotion Consent",
        selection=_CONSENT_SELECTION,
        compute="_compute_consent",
        store=True,
        compute_sudo=True,
        help=(
            "The strictest parental consent of the students of this "
            "artifact to use it for promotion, of the school of the "
            "artifact."
        ),
    )
    limited_publication_student_ids = fields.Many2many(
        string="Students With Limited Publication Consent",
        comodel_name="school_student",
        compute="_compute_publication_student_ids",
        compute_sudo=True,
        help=(
            "The students who allow the publication of this artifact "
            "only in a limited way. Check their preference before "
            "publishing."
        ),
    )
    refused_publication_student_ids = fields.Many2many(
        string="Students Refusing Publication",
        comodel_name="school_student",
        compute="_compute_publication_student_ids",
        compute_sudo=True,
        help="The students who withdrew the consent to publish this artifact.",
    )

    showcase_stage_id = fields.Many2one(
        string="Showcase Stage",
        comodel_name="school_learning_artifact_showcase_stage",
        ondelete="restrict",
        tracking=True,
        copy=False,
        group_expand="_read_group_showcase_stage_ids",
        domain="['|', ('school_ids', '=', False), ('school_ids', 'in', school_id)]",
        help=(
            "The stage of the artifact on the showcase board. Moving "
            "into a stage may require an eligible curation status, a "
            "publication consent that allows the showcase, or "
            "membership of a group, as configured on the stage. Every "
            "move is logged in the chatter with the user and the time."
        ),
    )
    showcase_channel_ids = fields.Many2many(
        string="Planned Channels",
        comodel_name="school_learning_artifact_showcase_channel",
        relation="school_la_showcase_planned_channel_rel",
        column1="artifact_id",
        column2="channel_id",
        domain="['|', ('school_ids', '=', False), ('school_ids', 'in', school_id)]",
        help="The channels planned to showcase this artifact.",
    )
    production_ids = fields.One2many(
        string="Showcase Productions",
        comodel_name="school_learning_artifact_showcase_production",
        inverse_name="artifact_id",
        help="The content produced for each channel of the showcase.",
    )
    actual_channel_ids = fields.Many2many(
        string="Actual Channels",
        comodel_name="school_learning_artifact_showcase_channel",
        relation="school_la_showcase_actual_channel_rel",
        column1="artifact_id",
        column2="channel_id",
        domain="['|', ('school_ids', '=', False), ('school_ids', 'in', school_id)]",
        help=(
            "The channels through which the artifact was actually "
            "distributed, outside Odoo."
        ),
    )
    distribution_note = fields.Text(
        string="Distribution Note",
        help="Any remark about the distribution of the artifact.",
    )
    consent_review_required = fields.Boolean(
        string="Consent Review Required",
        compute="_compute_showcase_consent",
        store=True,
        compute_sudo=True,
        help=(
            "Checked when the publication consent of the artifact is "
            "limited and the school treats it as a review task."
        ),
    )
    consent_reviewed = fields.Boolean(
        string="Consent Reviewed",
        default=False,
        readonly=True,
        copy=False,
        help="Checked when a reviewer examined the limited consent.",
    )
    consent_reviewed_by_id = fields.Many2one(
        string="Consent Reviewed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
        help="The user who marked the limited consent as reviewed.",
    )
    showcase_consent_ok = fields.Boolean(
        string="Showcase Consent OK",
        compute="_compute_showcase_consent",
        store=True,
        compute_sudo=True,
        help=(
            "Checked when the parental consent allows the artifact into "
            "the showcase, following the consent policy of its school."
        ),
    )
    promotion_allowed = fields.Boolean(
        string="Promotion Allowed",
        compute="_compute_promotion_allowed",
        store=True,
        compute_sudo=True,
        help=(
            "Checked when the parental consent of every student allows "
            "the artifact to be used for promotion in full."
        ),
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Create artifacts and number them right away.

        The document number is generated at creation, not only when
        the curation starts, so that a teacher can quote the code of a
        draft artifact. Records saved with a manual number are kept.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        for vals in vals_list:
            if vals.get("ethics_result"):
                vals["ethics_assessor_id"] = self.env.uid
        records = super().create(vals_list)
        for record in records.sudo():
            if record.name == "/":
                record._create_sequence()
        return records

    def write(self, vals):
        """Write artifacts and record who set the ethics result.

        :param vals: values to write
        :return: True
        :raises UserError: when the user may not set the ethics result
            or may not move the artifact into the showcase stage
        """
        if "ethics_result" in vals:
            self._check_ethics_assessor()
            assessor_id = self.env.uid if vals["ethics_result"] else False
            vals = dict(vals, ethics_assessor_id=assessor_id)
        if vals.get("showcase_stage_id") and not self.env.context.get(
            "showcase_stage_assignment"
        ):
            self._check_showcase_stage_move(vals["showcase_stage_id"])
        return super().write(vals)

    def _check_ethics_assessor(self):
        """Reject setting the ethics result outside the allowed groups.

        Nothing is checked for the superuser or for a rubric that lists
        no ethics assessor group.

        :raises UserError: when the active user may not set the result
        """
        if self.env.uid == SUPERUSER_ID:
            return
        user_groups = self.env.user.groups_id
        for record in self:
            allowed = record.rubric_id.ethics_assessor_group_ids
            if allowed and not (allowed & user_groups):
                record._raise_curation_error(
                    _("You are not allowed to set the ethics result"),
                    _("Ask a user in the ethics assessor groups to do it"),
                )

    @api.depends("school_id")
    def _compute_rubric_id(self):
        """Pick the rubric that applies to the school of the artifact.

        The active rubric listing the school wins. Otherwise the
        active rubric without schools is the fallback. The field stays
        empty when neither exists.
        """
        obj_rubric = self.env["school_learning_artifact_rubric"]
        for record in self:
            result = False
            if record.school_id:
                rubric = obj_rubric.search(
                    record._get_rubric_criteria(), order="id asc", limit=1
                )
                if not rubric:
                    rubric = obj_rubric.search(
                        record._get_fallback_rubric_criteria(),
                        order="id asc",
                        limit=1,
                    )
                if rubric:
                    result = rubric
            record.rubric_id = result

    def _get_rubric_criteria(self):
        """Build the search domain for the rubric of the school.

        Extension point: override to narrow the rubric choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("school_ids", "in", [self.school_id.id]),
        ]

    def _get_fallback_rubric_criteria(self):
        """Build the search domain for the fallback rubric.

        Extension point: override to narrow the fallback choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("school_ids", "=", False),
        ]

    @api.depends("score_ids.score")
    def _compute_total_score(self):
        """Sum the scores of all aspects."""
        for record in self:
            result = 0
            for score in record.score_ids:
                result += score.score
            record.total_score = result

    @api.depends(
        "ethics_result",
        "total_score",
        "score_ids.score",
        "score_ids.criterion_id",
        "rubric_id",
        "rubric_id.ethics_fail_status_id",
        "rubric_id.knockout_status_id",
        "rubric_id.criterion_ids.knockout_score",
        "rubric_id.threshold_ids.min_total",
        "rubric_id.threshold_ids.status_id",
    )
    def _compute_curation_status_id(self):
        """Derive the curation status from the rubric.

        A failed ethics gate gives the ethics fail status. Otherwise
        a score at or below the knockout score of its aspect gives the
        knockout status. Otherwise the threshold with the highest
        minimum that the total reaches gives its status.
        """
        for record in self:
            result = False
            rubric = record.rubric_id
            if rubric:
                result = record._get_curation_status(rubric)
            record.curation_status_id = result

    def _get_curation_status(self, rubric):
        """Return the curation status of the artifact for a rubric.

        Extension point: override to change how the status is derived.

        :param rubric: the ``school_learning_artifact_rubric`` in use
        :return: the status record, or False when none applies
        """
        self.ensure_one()
        result = False
        if self.ethics_result == "fail":
            result = rubric.ethics_fail_status_id
        elif rubric.knockout_status_id and self._has_knockout_score():
            result = rubric.knockout_status_id
        else:
            thresholds = rubric.threshold_ids.filtered(
                lambda r: r.min_total <= self.total_score
            )
            if thresholds:
                result = thresholds.sorted(
                    key=lambda r: (r.min_total, r.id), reverse=True
                )[0].status_id
        return result

    def _has_knockout_score(self):
        """Tell whether a given score knocks the artifact out.

        :return: True when a scored aspect with a knockout score has a
            score at or below it
        """
        self.ensure_one()
        result = False
        for score in self.score_ids:
            knockout = score.criterion_id.knockout_score
            if knockout and score.score and score.score <= knockout:
                result = True
        return result

    @api.depends("grade_id")
    def _compute_graduate_profile_id(self):
        """Pick the first active graduate profile covering the grade.

        Profiles are ordered by ``sequence``. The field stays empty
        when no active profile lists the grade of the class.
        """
        obj_profile = self.env["school_graduate_profile"]
        for record in self:
            result = False
            if record.grade_id:
                profile = obj_profile.search(
                    record._get_graduate_profile_criteria(),
                    order="sequence asc, id asc",
                    limit=1,
                )
                if profile:
                    result = profile
            record.graduate_profile_id = result

    def _get_graduate_profile_criteria(self):
        """Build the search domain for the graduate profile.

        Extension point: override to narrow the profile choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("grade_ids", "in", [self.grade_id.id]),
        ]

    @api.depends("description")
    def _compute_description_word_count(self):
        """Count the words of the description.

        Words are the whitespace separated chunks of ``description``.
        """
        for record in self:
            result = 0
            if record.description:
                result = len(record.description.split())
            record.description_word_count = result

    @api.depends("school_id", "school_id.branch_id")
    def _compute_allowed_component_ids(self):
        """List the components usable for the school of the artifact.

        A component applies when its program is active and belongs to
        the branch of the selected school. A school without a branch
        has no component to choose.
        """
        obj_component = self.env["school_distinctive_program_component"]
        for record in self:
            result = []
            if record.school_id.branch_id:
                result = obj_component.search(record._get_allowed_component_criteria())
            record.allowed_component_ids = result

    def _get_allowed_component_criteria(self):
        """Build the search domain for the allowed components.

        Extension point: override to widen or narrow the choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("program_id.branch_id", "=", self.school_id.branch_id.id),
            ("program_id.active", "=", True),
        ]

    @api.depends("school_id")
    def _compute_allowed_dimension_ids(self):
        """List the dimensions usable for the school of the artifact.

        A dimension applies when it lists the school or lists no
        school at all.
        """
        obj_dimension = self.env["school_learning_artifact_dimension"]
        for record in self:
            result = []
            if record.school_id:
                result = obj_dimension.search(record._get_allowed_school_criteria())
            record.allowed_dimension_ids = result

    @api.depends("school_id")
    def _compute_allowed_phase_ids(self):
        """List the phases usable for the school of the artifact.

        A phase applies when it lists the school or lists no school
        at all.
        """
        obj_phase = self.env["school_learning_artifact_phase"]
        for record in self:
            result = []
            if record.school_id:
                result = obj_phase.search(record._get_allowed_school_criteria())
            record.allowed_phase_ids = result

    def _get_allowed_school_criteria(self):
        """Build the search domain for school scoped master data.

        Used for dimensions and phases: records without schools apply
        to every school, the others only to the schools they list.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            "|",
            ("school_ids", "=", False),
            ("school_ids", "in", [self.school_id.id]),
        ]

    @api.depends(*_CONSENT_DEPENDS)
    def _compute_consent(self):
        """Derive the parental consent of the artifact per usage.

        For each usage the strictest consent of the students of the
        artifact wins, in the order refused, not recorded, limited,
        full. An artifact without students has no consent recorded.
        """
        for record in self:
            result = record._get_consent_summary()
            record.inventory_consent = result["inventory"]
            record.assessment_consent = result["assessment"]
            record.publication_consent = result["publication"]
            record.promotion_consent = result["promotion"]

    @api.depends(*_CONSENT_DEPENDS)
    def _compute_publication_student_ids(self):
        """List the students who limit or refuse the publication."""
        for record in self:
            limited = record._get_students_by_consent("publication", "limited")
            refused = record._get_students_by_consent("publication", "refused")
            record.limited_publication_student_ids = limited
            record.refused_publication_student_ids = refused

    def _get_consent_summary(self):
        """Aggregate the consent of the students per usage.

        :return: dictionary of the consent state of each usage
        """
        self.ensure_one()
        result = dict.fromkeys(_CONSENT_USAGES, "unknown")
        if self.student_ids:
            student_states = [
                self._get_student_consent_states(student)
                for student in self.student_ids
            ]
            for usage in _CONSENT_USAGES:
                result[usage] = max(
                    (states[usage] for states in student_states),
                    key=_CONSENT_RANK.get,
                )
        return result

    def _get_students_by_consent(self, usage, state):
        """Return the students of the artifact with a given consent.

        :param usage: one of the usages of the artifact consent
        :param state: ``full``, ``limited``, ``refused`` or ``unknown``
        :return: ``school_student`` recordset
        """
        self.ensure_one()
        return self.student_ids.filtered(
            lambda r: self._get_student_consent_states(r)[usage] == state
        )

    def _get_student_consent_states(self, student):
        """Return the latest consent of a student per usage.

        Only the consents of the contact of the student for the school
        of the artifact count. Per usage the latest consent event, by
        consent date and then by id, decides: a granted consent is full
        or limited by its level, a withdrawn consent is refused, and
        no consent at all is not recorded.

        :param student: the ``school_student`` to look up
        :return: dictionary of the consent state of each usage
        """
        self.ensure_one()
        result = dict.fromkeys(_CONSENT_USAGES, "unknown")
        consents = (
            self.env["res.partner.consent"]
            .sudo()
            .search(self._get_consent_criteria(student))
        )
        consents = consents.sorted(key=lambda r: (r.consent_date, r.id), reverse=True)
        seen = set()
        for consent in consents:
            usage = consent.purpose_id.learning_artifact_usage
            if usage in seen:
                continue
            seen.add(usage)
            if consent.consent_type == "withdraw":
                result[usage] = "refused"
            elif consent.consent_level == "limited":
                result[usage] = "limited"
            else:
                result[usage] = "full"
        return result

    def _get_consent_criteria(self, student):
        """Build the search domain for the consents of a student.

        Extension point: override to narrow the consents that count.

        :param student: the ``school_student`` to look up
        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return [
            ("partner_id", "=", student.contact_id.id),
            ("school_id", "=", self.school_id.id),
            ("purpose_id.learning_artifact_usage", "!=", False),
        ]

    @api.onchange("school_id")
    def onchange_grade_class_id(self):
        self.grade_class_id = False

    @api.onchange("school_id")
    def onchange_student_ids(self):
        self.student_ids = [(5,)]

    @api.onchange("school_id")
    def onchange_learning_area_id(self):
        self.learning_area_id = False

    @api.onchange("school_id")
    def onchange_primary_component_id(self):
        self.primary_component_id = False

    @api.onchange("school_id")
    def onchange_secondary_component_id(self):
        self.secondary_component_id = False

    @api.onchange("school_id")
    def onchange_dimension_id(self):
        self.dimension_id = False

    @api.onchange("school_id")
    def onchange_phase_id(self):
        self.phase_id = False

    @ssi_decorator.pre_confirm_check()
    def _10_check_submit_students(self):
        """Require at least one student before submission.

        Called by ``mixin.transaction_confirm`` before the artifact
        moves to ``confirm``.
        """
        self.ensure_one()
        if not self.student_ids:
            self._raise_submit_error(
                _("No student is selected"),
                _("Select at least one student"),
            )

    @ssi_decorator.pre_confirm_check()
    def _20_check_submit_required_data(self):
        """Require the descriptive data before submission.

        Called by ``mixin.transaction_confirm`` before the artifact
        moves to ``confirm``. The learning area, the category, the
        description and the link are always required. The component,
        the dimension and the phase are required only when the flags
        of the school switch them on.
        """
        self.ensure_one()
        for field_name in self._get_submit_required_fields():
            if not self[field_name]:
                self._raise_submit_error(
                    _("%s is empty") % self._fields[field_name].string,
                    _("Fill in %s") % self._fields[field_name].string,
                )

    def _get_submit_required_fields(self):
        """Return the names of the fields required to submit.

        Extension point: override to add or remove required fields.
        The three optional fields are added according to the flags of
        ``school_id``.

        :return: list of field names
        """
        self.ensure_one()
        result = [
            "learning_area_id",
            "category_id",
            "description",
            "link_url",
        ]
        school = self.school_id
        if school.learning_artifact_require_component:
            result.append("primary_component_id")
        if school.learning_artifact_require_dimension:
            result.append("dimension_id")
        if school.learning_artifact_require_phase:
            result.append("phase_id")
        return result

    @ssi_decorator.pre_confirm_check()
    def _30_check_submit_link_prefix(self):
        """Require the link to start with the prefix of the school.

        Called by ``mixin.transaction_confirm`` before the artifact
        moves to ``confirm``. Nothing is checked when the school
        defines no link prefix.
        """
        self.ensure_one()
        prefix = self.school_id.learning_artifact_link_prefix
        if prefix and self.link_url and not self.link_url.startswith(prefix):
            self._raise_submit_error(
                _("The Link must start with %s.") % prefix,
                _("Correct the Link so that it starts with %s") % prefix,
            )

    @ssi_decorator.pre_confirm_check()
    def _40_check_submit_inventory_consent(self):
        """Require the inventory consent of the students before submission.

        Called by ``mixin.transaction_confirm`` before the artifact
        moves to ``confirm``. A student who refused the inventory
        consent always blocks the submission. A student without any
        inventory consent recorded blocks it only when the school
        switches that on.
        """
        self.ensure_one()
        refused = self._get_students_by_consent("inventory", "refused")
        if refused:
            self._raise_submit_error(
                _("%s refused the inventory consent")
                % ", ".join(refused.mapped("name")),
                _("Remove the student from the artifact"),
            )
        if self.school_id.learning_artifact_require_inventory_consent:
            unknown = self._get_students_by_consent("inventory", "unknown")
            if unknown:
                self._raise_submit_error(
                    _("%s has no inventory consent recorded")
                    % ", ".join(unknown.mapped("name")),
                    _("Record the inventory consent of the student"),
                )

    def _raise_submit_error(self, problem, solution):
        """Raise the standard error of the submit checks.

        :param problem: what is wrong, already translated
        :param solution: how to fix it, already translated
        :raises UserError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Submit learning artifact for curation
Database ID: %s
Problem: %s
Solution: %s
"""
            )
            % (self.id, problem, solution)
        )
        raise UserError(error_message)

    @ssi_decorator.post_open_action()
    def _10_create_score_rows(self):
        """Create one score row per aspect of the rubric.

        Post-open hook: runs once the artifact reaches ``open``. Rows
        are created only when the artifact has none yet, so a reopened
        artifact keeps the scores it already has.
        """
        self.ensure_one()
        if self.rubric_id and not self.score_ids:
            self.write(
                {
                    "score_ids": [
                        (0, 0, {"criterion_id": criterion.id})
                        for criterion in self.rubric_id.criterion_ids
                    ]
                }
            )

    @ssi_decorator.pre_done_check()
    def _10_check_curation_ethics(self):
        """Require the ethics result and the scores before finishing.

        Pre-done hook: the rubric and the ethics result are always
        required. When the ethics gate passed, every aspect must also
        be scored.

        :raises UserError: when the curation data is incomplete
        """
        self.ensure_one()
        if not self.rubric_id:
            self._raise_curation_error(
                _("No rubric applies to the school"),
                _("Create a rubric for the school or a fallback rubric"),
            )
        if not self.ethics_result:
            self._raise_curation_error(
                _("Ethics Result is empty"),
                _("Set the Ethics Result"),
            )
        if self.ethics_result == "pass":
            for score in self.score_ids:
                if not score.score:
                    self._raise_curation_error(
                        _("Aspect %s is not scored") % score.criterion_id.display_name,
                        _("Score every aspect"),
                    )

    @ssi_decorator.pre_done_check()
    def _20_check_curation_note(self):
        """Require the note that the curation status asks for.

        Pre-done hook: a status in the revision category requires the
        recommendation, and a status in the not eligible category
        requires the curator note as the reason of the archive.

        :raises UserError: when the required note is empty
        """
        self.ensure_one()
        category = self.curation_status_category
        if category == "revision" and not self.recommendation:
            self._raise_curation_error(
                _("Recommendation is empty"),
                _("Write a recommendation for the revision"),
            )
        if category == "rejected" and not self.curator_note:
            self._raise_curation_error(
                _("Curator Note is empty"),
                _("Write the reason of the archive in the Curator Note"),
            )

    @ssi_decorator.pre_done_check()
    def _30_check_distinct_assessors(self):
        """Reject one person assessing both assessor slots.

        Pre-done hook: runs only when the rubric requires distinct
        assessors. The ethics gate counts as the secondary slot.

        :raises UserError: when a user assessed both slots
        """
        self.ensure_one()
        rubric = self.rubric_id
        if not rubric.require_distinct_assessors:
            return
        primary = self._get_slot_assessors("primary")
        secondary = self._get_slot_assessors("secondary")
        secondary |= self.ethics_assessor_id
        common = primary & secondary
        if common:
            self._raise_curation_error(
                _("%s assessed both the primary and secondary slots")
                % ", ".join(common.mapped("name")),
                _("Let different users assess the primary and secondary slots"),
            )

    def _get_slot_assessors(self, slot):
        """Return the users who scored the aspects of an assessor slot.

        :param slot: ``primary`` or ``secondary``
        :return: ``res.users`` recordset
        """
        self.ensure_one()
        scores = self.score_ids.filtered(lambda r: r.criterion_id.assessor_slot == slot)
        return scores.mapped("assessor_id")

    @ssi_decorator.pre_done_check()
    def _40_check_creator_assessment(self):
        """Reject the responsible user assessing the own artifact.

        Pre-done hook: runs only when the rubric forbids the creator
        to assess.

        :raises UserError: when the responsible user assessed it
        """
        self.ensure_one()
        if not self.rubric_id.forbid_creator_assessment:
            return
        assessors = self.score_ids.mapped("assessor_id") | self.ethics_assessor_id
        if self.user_id and self.user_id in assessors:
            self._raise_curation_error(
                _("The responsible user assessed the artifact"),
                _("Let another user assess the artifact"),
            )

    @api.model
    def _read_group_showcase_stage_ids(self, stages, domain, order):
        """Show every active showcase stage as a column of the board.

        Used as ``group_expand`` of ``showcase_stage_id`` so that empty
        stages stay visible and a card can be dragged into them.

        :param stages: stages that already hold an artifact
        :param domain: domain of the board
        :param order: order of the stages
        :return: ``school_learning_artifact_showcase_stage`` recordset
        """
        return stages.search([], order=order)

    @api.depends(*_SHOWCASE_CONSENT_DEPENDS)
    def _compute_showcase_consent(self):
        """Decide whether the consent allows the showcase.

        An artifact whose internal assessment consent is refused never
        reaches the showcase. Otherwise the effective publication
        consent decides: a full consent is accepted, a limited consent
        is accepted when the school accepts it as a minimum or treats
        it as a review task, and in the latter case only after a
        reviewer marked it as reviewed. A refused or missing consent is
        never accepted.
        """
        for record in self:
            effective = record._get_showcase_publication_consent()
            school = record.school_id
            treatment_review = school.showcase_limited_treatment == "review"
            result = False
            if record.assessment_consent != "refused":
                if effective == "full":
                    result = True
                elif effective == "limited":
                    if treatment_review:
                        result = record.consent_reviewed
                    else:
                        result = school.showcase_min_publication_consent == "limited"
            record.showcase_consent_ok = result
            record.consent_review_required = bool(
                effective == "limited" and treatment_review
            )

    def _get_showcase_publication_consent(self):
        """Return the publication consent that counts for the showcase.

        It is the stored aggregate publication consent. When the school
        ignores the students who refused the publication, it is
        calculated again over the other students; with no student left
        the consent is not recorded.

        :return: ``full``, ``limited``, ``refused`` or ``unknown``
        """
        self.ensure_one()
        result = self.publication_consent
        if self.school_id.showcase_exclude_refused_member:
            remaining = self.student_ids - self._get_students_by_consent(
                "publication", "refused"
            )
            result = "unknown"
            if remaining:
                result = max(
                    (
                        self._get_student_consent_states(student)["publication"]
                        for student in remaining
                    ),
                    key=_CONSENT_RANK.get,
                )
        return result

    @api.depends("promotion_consent")
    def _compute_promotion_allowed(self):
        """Allow the promotion only with a full promotion consent."""
        for record in self:
            record.promotion_allowed = record.promotion_consent == "full"

    def action_mark_consent_reviewed(self):
        """Mark the limited publication consent as reviewed.

        Records the reviewer on the artifact. When the school names a
        consent reviewer group, only its users may do it.

        :return: True
        :raises UserError: when the user is outside the reviewer group
        """
        for record in self:
            record._check_consent_reviewer()
            record.write(
                {
                    "consent_reviewed": True,
                    "consent_reviewed_by_id": self.env.uid,
                }
            )
        return True

    def _check_consent_reviewer(self):
        """Reject marking the consent as reviewed outside the group.

        Nothing is checked for the superuser or for a school that
        names no consent reviewer group.

        :raises UserError: when the active user is not a reviewer
        """
        self.ensure_one()
        group = self.school_id.showcase_consent_reviewer_group_id
        if (
            group
            and self.env.uid != SUPERUSER_ID
            and group not in self.env.user.groups_id
        ):
            self._raise_showcase_error(
                _("You are not allowed to review the consent"),
                _("Ask a user in the group %s to do it") % group.display_name,
            )

    def _check_showcase_stage_move(self, stage_id):
        """Reject a move into a showcase stage whose rules are not met.

        A stage may require an eligible curation status, a publication
        consent that allows the showcase, and membership of one of its
        allowed groups. The superuser is exempt from the group rule.

        :param stage_id: id of the stage the artifact moves into
        :raises UserError: when a rule of the stage is not met
        """
        stage = self.env["school_learning_artifact_showcase_stage"].browse(stage_id)
        for record in self:
            if stage.require_eligible and (
                record.curation_status_category != "eligible"
            ):
                record._raise_showcase_error(
                    _("The curation status of the artifact is not eligible"),
                    _("Move the artifact into %s only when it is eligible")
                    % stage.display_name,
                )
            if stage.require_publication_consent and not record.showcase_consent_ok:
                record._raise_showcase_error(
                    _("The parental consent does not allow the showcase"),
                    _("Obtain the consent required by the school first"),
                )
            allowed = stage.allowed_group_ids
            if (
                allowed
                and self.env.uid != SUPERUSER_ID
                and not (allowed & self.env.user.groups_id)
            ):
                record._raise_showcase_error(
                    _("You are not allowed to move the artifact into %s")
                    % stage.display_name,
                    _("Ask a user in the allowed groups of the stage to do it"),
                )

    def _raise_showcase_error(self, problem, solution):
        """Raise the standard error of the showcase checks.

        :param problem: what is wrong, already translated
        :param solution: how to fix it, already translated
        :raises UserError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Move learning artifact on the showcase board
Database ID: %s
Problem: %s
Solution: %s
"""
            )
            % (self.id, problem, solution)
        )
        raise UserError(error_message)

    @ssi_decorator.post_done_action()
    def _10_assign_initial_showcase_stage(self):
        """Give a curated artifact its first showcase stage.

        Post-done hook: the active stage with the lowest sequence that
        applies to the school is assigned when the artifact has no
        stage yet. The stage rules are not checked for this first
        assignment, which is not a move made by a user.
        """
        self.ensure_one()
        if self.showcase_stage_id:
            return
        stage = self.env["school_learning_artifact_showcase_stage"].search(
            self._get_initial_showcase_stage_criteria(),
            order="sequence asc, id asc",
            limit=1,
        )
        if stage:
            self.with_context(showcase_stage_assignment=True).write(
                {"showcase_stage_id": stage.id}
            )

    def _get_initial_showcase_stage_criteria(self):
        """Build the search domain for the first showcase stage.

        Extension point: override to narrow the stage choice.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        return self._get_allowed_school_criteria()

    def _prepare_done_data(self):
        """Add the curator and the time to the data of the done state.

        :return: dictionary of values to write
        """
        result = super()._prepare_done_data()
        result.update(
            {
                "curated_by_id": self.env.uid,
                "date_curated": fields.Datetime.now(),
            }
        )
        return result

    def _prepare_restart_data(self):
        """Count the revision when a curated artifact is reopened.

        :return: dictionary of values to write
        """
        result = super()._prepare_restart_data()
        if self.state == "done":
            result["revision_count"] = self.revision_count + 1
        return result

    def _raise_curation_error(self, problem, solution):
        """Raise the standard error of the curation checks.

        :param problem: what is wrong, already translated
        :param solution: how to fix it, already translated
        :raises UserError: always
        """
        self.ensure_one()
        error_message = (
            _(
                """
Context: Finish curation of learning artifact
Database ID: %s
Problem: %s
Solution: %s
"""
            )
            % (self.id, problem, solution)
        )
        raise UserError(error_message)

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
