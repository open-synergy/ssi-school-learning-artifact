# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator

_DRAFT_EDITABLE = {
    "draft": [
        ("readonly", False),
    ],
}


class SchoolLearningArtifact(models.Model):
    """
    Represents one Learning Artifact: a photo, video or document that
    records a learning activity, project or achievement of one or more
    students. A teacher records the artifact (Draft), submits it for
    curation (Waiting for Approval), may withdraw it again with Restart
    while the curator has not started yet, and the curator starts the
    curation by approving it (On Progress). The workflow is Draft ->
    Confirm -> Approve -> Open, plus Cancel from draft, confirm and
    reject. Every school specific choice (areas, categories,
    dimensions, phases, distinctive programs, graduate profiles, link
    prefix and the required-field switches) is configuration data kept
    per school or per branch, never hard-coded in this module.
    """

    _name = "school_learning_artifact"
    _inherit = [
        "mixin.transaction_cancel",
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

    _statusbar_visible_label = "draft,confirm,open"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

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

    @api.model_create_multi
    def create(self, vals_list):
        """Create artifacts and number them right away.

        The document number is generated at creation, not only when
        the curation starts, so that a teacher can quote the code of a
        draft artifact. Records saved with a manual number are kept.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        records = super().create(vals_list)
        for record in records.sudo():
            if record.name == "/":
                record._create_sequence()
        return records

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
