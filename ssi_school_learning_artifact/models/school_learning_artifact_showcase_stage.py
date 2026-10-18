# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolLearningArtifactShowcaseStage(
    models.Model
):  # pylint: disable=too-few-public-methods
    """
    Represents a stage of the showcase board of the curated learning
    artifacts, for example selected, in production or distributed. The
    stages, their order and the rules to move an artifact into them are
    configuration data. A stage can be limited to some schools or left
    open to every school.
    """

    _name = "school_learning_artifact_showcase_stage"
    _inherit = ["mixin.master_data"]
    _description = "School Learning Artifact Showcase Stage"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help=(
            "Order of the stage on the showcase board. The lowest "
            "sequence is the first stage given to a curated artifact."
        ),
    )
    fold = fields.Boolean(
        string="Folded in Board",
        default=False,
        help="If checked, the column of this stage is folded on the board.",
    )
    school_ids = fields.Many2many(
        string="Schools",
        comodel_name="school",
        relation="school_la_showcase_stage_school_rel",
        column1="stage_id",
        column2="school_id",
        help=(
            "Schools that can use this stage. Leave empty to make the "
            "stage available to every school."
        ),
    )
    require_eligible = fields.Boolean(
        string="Require Eligible Curation Status",
        default=False,
        help=(
            "If checked, an artifact can move into this stage only when "
            "the category of its curation status is Eligible."
        ),
    )
    require_publication_consent = fields.Boolean(
        string="Require Publication Consent",
        default=False,
        help=(
            "If checked, an artifact can move into this stage only when "
            "the parental consent allows the showcase, following the "
            "consent policy of its school."
        ),
    )
    allowed_group_ids = fields.Many2many(
        string="Allowed Groups",
        comodel_name="res.groups",
        relation="school_la_showcase_stage_group_rel",
        column1="stage_id",
        column2="group_id",
        help=(
            "Groups whose users can move an artifact into this stage. "
            "Leave empty to let anyone who may edit the artifact do it."
        ),
    )
