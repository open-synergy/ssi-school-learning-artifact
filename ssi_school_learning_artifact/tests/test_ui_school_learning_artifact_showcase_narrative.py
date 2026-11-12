# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactShowcaseNarrative(HttpSavepointCase):
    """Tour tests for the showcase narrative work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 6 tours.

        One school with a rubric that makes a score of 3 eligible, a
        showcase channel without word limit and an approval detail on
        the approval template of the showcase production (the admin
        approves) are created. Six curated artifacts are built through
        the real action methods, one per tour, each with one showcase
        production moved through the action methods to the status the
        tour starts from. ``user_id`` is set to ``base.user_admin`` so
        the tour session, which is a coordinator, can see them.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR NR Grade Type",
                "code": "TOURNRGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR NR School",
                "code": "TOURNRSC",
                "grade_type_id": grade_type.id,
                "showcase_limited_treatment": "review",
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR NR Grade",
                "code": "TOURNRGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR NR Class",
                "code": "TOURNRCL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR NR Year",
                "code": "TOURNRAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.contact = cls.env["res.partner"].create({"name": "TOUR NR Student Contact"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR NR Student",
                "code": "TOURNRST",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR NR Area",
                "code": "TOURNRAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        cls.category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR NR Category",
                "code": "TOURNRCA",
            }
        )
        obj_status = cls.env["school_learning_artifact_curation_status"]
        eligible = obj_status.create(
            {
                "name": "TOUR NR Eligible",
                "code": "TOURNREL",
                "category": "eligible",
            }
        )
        rejected = obj_status.create(
            {
                "name": "TOUR NR Rejected",
                "code": "TOURNRRJ",
                "category": "rejected",
            }
        )
        cls.env["school_learning_artifact_rubric"].create(
            {
                "name": "TOUR NR Rubric",
                "code": "TOURNRRB",
                "school_ids": [(6, 0, cls.school.ids)],
                "ethics_fail_status_id": rejected.id,
                "criterion_ids": [
                    (
                        0,
                        0,
                        {
                            "code": "TA1",
                            "name": "TOUR NR Aspect",
                            "aspect_type": "score",
                            "level_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 10,
                                        "score": 1,
                                        "name": "TOUR NR Level One",
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 20,
                                        "score": 2,
                                        "name": "TOUR NR Level Two",
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 30,
                                        "score": 3,
                                        "name": "TOUR NR Level Three",
                                    },
                                ),
                            ],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "code": "TG1",
                            "name": "TOUR NR Ethics Gate",
                            "aspect_type": "gate",
                            "assessor_slot": "secondary",
                            "level_ids": [
                                (0, 0, {"sequence": 10, "name": "TOUR NR Gate Pass"}),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 20,
                                        "name": "TOUR NR Gate Fail",
                                        "is_fail": True,
                                    },
                                ),
                            ],
                        },
                    ),
                ],
                "threshold_ids": [
                    (0, 0, {"min_total": 3, "status_id": eligible.id}),
                ],
            }
        )
        cls.channel = cls.env["school_learning_artifact_showcase_channel"].create(
            {
                "name": "TOUR NR Channel",
                "code": "TOURNRCH",
                "school_ids": [(6, 0, cls.school.ids)],
            }
        )
        cls.env["approval.template_detail"].create(
            {
                "template_id": cls.env.ref(
                    "ssi_school_learning_artifact."
                    "approval_template_school_learning_artifact_showcase_production"
                ).id,
                "sequence": 1,
                "approver_selection_method": "use_user",
                "approver_user_ids": [(6, 0, cls.admin.ids)],
            }
        )

        # One production per tour, brought to the status the tour needs.
        cls._create_production("TOUR NR Return Teacher", [])
        cls._create_production("TOUR NR Submit", ["assign"])
        cls._create_production("TOUR NR Request", ["assign", "submit"])
        cls._create_production("TOUR NR Return", ["assign", "submit"])
        cls._create_production("TOUR NR Approve", ["assign", "submit", "request"])
        cls._create_production("TOUR NR Reject", ["assign", "submit", "request"])

    @classmethod
    def _create_production(cls, activity_name, steps):
        """Create a curated artifact and a production moved by steps.

        The caches are invalidated between the transitions because the
        policy fields are cached by the previous status.

        :param activity_name: unique activity name used as the row
            marker by the tour.
        :param steps: list of ``assign``, ``submit`` and ``request``
            applied in order to the new production.
        :return: the new production record.
        """
        artifact = cls._create_curated_artifact(activity_name)
        production = cls.env["school_learning_artifact_showcase_production"].create(
            {"artifact_id": artifact.id, "channel_id": cls.channel.id}
        )
        methods = {
            "assign": "action_assign_to_teacher",
            "submit": "action_submit_narrative",
            "request": "action_request_narrative_approval",
        }
        for step in steps:
            getattr(production.with_user(cls.admin), methods[step])()
            production.invalidate_cache()
        return production

    @classmethod
    def _create_curated_artifact(cls, activity_name, student=None):
        """Create an artifact and move it to Curated.

        ``user_id`` is set explicitly to ``base.user_admin`` because
        ``cls.env`` runs as SUPERUSER and the internal user record
        rule would otherwise hide the record from the tour session.
        The caches are invalidated between the transitions because the
        policy fields are cached while the record is still a draft.

        :param activity_name: unique activity name used as the row
            marker by the tour.
        :param student: student of the artifact, the limited consent
            student when omitted.
        :return: the ``school_learning_artifact`` record Curated.
        """
        student = student or cls.student
        artifact = cls.env["school_learning_artifact"].create(
            {
                "school_id": cls.school.id,
                "academic_year_id": cls.year.id,
                "grade_class_id": cls.grade_class.id,
                "activity_name": activity_name,
                "media_type": "photo",
                "user_id": cls.admin.id,
                "student_ids": [(6, 0, student.ids)],
                "learning_area_id": cls.area.id,
                "category_id": cls.category.id,
                "description": "one two three",
                "link_url": "https://drive.example.com/file",
            }
        )
        artifact.with_user(cls.admin).action_confirm()
        artifact.invalidate_cache()
        artifact.with_user(cls.admin).action_approve_approval()
        artifact.invalidate_cache()
        cls._answer_curation(artifact, "TOUR NR Level Three")
        artifact.invalidate_cache()
        artifact.with_user(cls.admin).action_done()
        artifact.invalidate_cache()
        return artifact

    @classmethod
    def _answer_curation(cls, artifact, level_name):
        """Pass the ethics gate and pick a level of the scored aspect.

        :param artifact: the artifact that is On Progress.
        :param level_name: name of the level to pick on the scored
            aspect.
        :return: None
        """
        obj_level = cls.env["school_learning_artifact_rubric_criterion_level"]
        # The gate rows come first: the scored aspects stay locked until
        # every gate row is answered with a passing level.
        rows = artifact.score_ids.sorted(lambda r: r.aspect_type != "gate")
        for row in rows:
            if row.aspect_type == "gate":
                level = obj_level.search(
                    [
                        ("criterion_id", "=", row.criterion_id.id),
                        ("is_fail", "=", False),
                    ]
                )
            else:
                level = obj_level.search(
                    [
                        ("criterion_id", "=", row.criterion_id.id),
                        ("name", "=", level_name),
                    ]
                )
            row.write({"level_id": level.id})

    def test_return_narrative_to_teacher(self):
        """Run the return to teacher tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/13-return-narrative-to-teacher.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "return_narrative_to_teacher",
            login="admin",
        )

    def test_submit_narrative(self):
        """Run the submit tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/14-submit-narrative.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "submit_narrative",
            login="admin",
        )

    def test_request_narrative_approval(self):
        """Run the request approval tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/15-request-narrative-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "request_narrative_approval",
            login="admin",
        )

    def test_return_narrative(self):
        """Run the return tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/16-return-narrative.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "return_narrative",
            login="admin",
        )

    def test_approve_narrative(self):
        """Run the approve tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/17-approve-narrative.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "approve_narrative",
            login="admin",
        )

    def test_reject_narrative(self):
        """Run the reject tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/18-reject-narrative.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "reject_narrative",
            login="admin",
        )
