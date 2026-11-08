# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class SchoolLearningArtifactCurationLoad(models.Model):
    """
    Read-only reporting model that lists one row for every aspect
    that an assessor assessed on a learning artifact, ethics gate
    aspects included, so the curation load of each person can be
    counted per aspect in a pivot. Backed by a plain SQL view, not
    stored; always reflects current data.
    """

    _name = "school_learning_artifact_curation_load"
    _description = "Learning Artifact Curation Load"
    _auto = False
    _order = "id desc"

    assessor_id = fields.Many2one(
        string="Assessor",
        comodel_name="res.users",
        readonly=True,
        help="The user who assessed the aspect.",
    )
    artifact_id = fields.Many2one(
        string="Learning Artifact",
        comodel_name="school_learning_artifact",
        readonly=True,
        help="The learning artifact that owns the assessed aspect.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        readonly=True,
        help="The school of the learning artifact.",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        readonly=True,
        help="The academic year of the learning artifact.",
    )
    grade_type_id = fields.Many2one(
        string="Grade Type",
        comodel_name="school_grade_type",
        readonly=True,
        help="The grade type of the class of the learning artifact.",
    )
    criterion_id = fields.Many2one(
        string="Aspect",
        comodel_name="school_learning_artifact_rubric_criterion",
        readonly=True,
        help="The rubric aspect that the assessor assessed.",
    )
    aspect_type = fields.Selection(
        string="Aspect Type",
        selection=[
            ("score", "Scored Aspect"),
            ("gate", "Ethics Gate"),
        ],
        readonly=True,
        help="Whether the aspect is scored or is an ethics gate.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        readonly=True,
        help="The state of the learning artifact.",
    )
    aspect_count = fields.Integer(
        string="Assessed Aspects",
        readonly=True,
        help="Always one: each row is one assessed aspect.",
    )

    def init(self):
        """Create the SQL view that backs this report model.

        Odoo calls this on every module install or update for an
        ``_auto = False`` model. The existing view is dropped first and
        recreated from ``_select_query``, so a changed query takes
        effect as soon as the module is updated.

        :return: None
        """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE VIEW %s AS (%s)""" % (self._table, self._select_query())
        )

    def _select_query(self):
        """Return the SQL SELECT that feeds the report view.

        Takes one row for each score row that has an assessor, joined
        to its artifact and its rubric aspect. The score row id is the
        row ``id``, so one report row equals one assessed aspect.
        Extension point: override to add columns or joins; every added
        column must be matched by a field declared on this model.

        :return: str containing the SELECT statement
        """
        return """
            SELECT
                score.id AS id,
                score.assessor_id AS assessor_id,
                score.artifact_id AS artifact_id,
                artifact.school_id AS school_id,
                artifact.academic_year_id AS academic_year_id,
                artifact.grade_type_id AS grade_type_id,
                score.criterion_id AS criterion_id,
                criterion.aspect_type AS aspect_type,
                artifact.state AS state,
                1 AS aspect_count
            FROM school_learning_artifact_score score
            JOIN school_learning_artifact artifact
                ON artifact.id = score.artifact_id
            JOIN school_learning_artifact_rubric_criterion criterion
                ON criterion.id = score.criterion_id
            WHERE score.assessor_id IS NOT NULL
        """
