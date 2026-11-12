# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged

LONG_LEVEL_TEXT = (
    "TOUR LC Level Three: the artifact shows a complete learning process, "
    "names the evidence behind every claim, explains what changed after "
    "each revision and closes with a reflection written by the student "
    "END-OF-LEVEL-TEXT"
)


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactCuration(HttpSavepointCase):
    """Tour tests for the curation work instructions of the artifact."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 3 tours.

        One school with its own rubric of a scored aspect and an ethics
        gate aspect is created, with an eligible, a revision, a not
        eligible and an archive status. The curate tour gets an
        artifact that is On Progress. The reopen tour gets an artifact
        that is Curated with the revision category. The final status
        tour gets an artifact that is On Progress again after one
        reopening. All move through the real action methods, and
        ``user_id`` is set to ``base.user_admin`` so the tour session
        can see them.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR LC Grade Type",
                "code": "TOURLCGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR LC School",
                "code": "TOURLCSC",
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR LC Grade",
                "code": "TOURLCGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR LC Class",
                "code": "TOURLCCL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR LC Year",
                "code": "TOURLCAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR LC Student Contact"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR LC Student",
                "code": "TOURLCST",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR LC Area",
                "code": "TOURLCAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        cls.category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR LC Category",
                "code": "TOURLCCA",
            }
        )
        obj_status = cls.env["school_learning_artifact_curation_status"]
        eligible = obj_status.create(
            {
                "name": "TOUR LC Eligible",
                "code": "TOURLCEL",
                "category": "eligible",
            }
        )
        revision = obj_status.create(
            {
                "name": "TOUR LC Revision",
                "code": "TOURLCRV",
                "category": "revision",
            }
        )
        rejected = obj_status.create(
            {
                "name": "TOUR LC Rejected",
                "code": "TOURLCRJ",
                "category": "rejected",
            }
        )
        obj_status.create(
            {
                "name": "TOUR LC Archive",
                "code": "TOURLCAC",
                "category": "archive",
            }
        )
        cls.rubric = cls.env["school_learning_artifact_rubric"].create(
            {
                "name": "TOUR LC Rubric",
                "code": "TOURLCRB",
                "school_ids": [(6, 0, cls.school.ids)],
                "ethics_fail_status_id": rejected.id,
                "criterion_ids": [
                    (
                        0,
                        0,
                        {
                            "code": "TA1",
                            "name": "TOUR Aspect One",
                            "aspect_type": "score",
                            "level_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 10,
                                        "score": 1,
                                        "name": "TOUR LC Level One",
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 20,
                                        "score": 2,
                                        "name": "TOUR LC Level Two",
                                    },
                                ),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 30,
                                        "score": 3,
                                        "name": LONG_LEVEL_TEXT,
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
                            "name": "TOUR LC Ethics Gate",
                            "aspect_type": "gate",
                            "assessor_slot": "secondary",
                            "level_ids": [
                                (0, 0, {"sequence": 10, "name": "TOUR LC Gate Pass"}),
                                (
                                    0,
                                    0,
                                    {
                                        "sequence": 20,
                                        "name": "TOUR LC Gate Fail",
                                        "is_fail": True,
                                    },
                                ),
                            ],
                        },
                    ),
                ],
                "threshold_ids": [
                    (0, 0, {"min_total": 3, "status_id": eligible.id}),
                    (0, 0, {"min_total": 1, "status_id": revision.id}),
                ],
            }
        )

        # 06-curate.md -- On Progress record to curate.
        cls.artifact_curate = cls._create_open_artifact("TOUR LC Curate Activity")

        # 07-reopen.md -- Curated record whose category is revision.
        cls.artifact_reopen = cls._create_open_artifact("TOUR LC Reopen Activity")
        cls.artifact_reopen.write({"recommendation": "Strengthen the reflection"})
        cls._answer_curation(cls.artifact_reopen, "TOUR LC Level Two")
        cls.artifact_reopen.invalidate_cache()
        cls.artifact_reopen.with_user(cls.admin).action_done()

        # 12-set-final-status.md -- On Progress record that was already
        # reopened once, so the revision limit of the rubric is reached.
        cls.artifact_final = cls._create_open_artifact("TOUR LC Final Status Activity")
        cls.artifact_final.write({"recommendation": "Strengthen the reflection"})
        cls._answer_curation(cls.artifact_final, "TOUR LC Level Two")
        cls.artifact_final.invalidate_cache()
        cls.artifact_final.with_user(cls.admin).action_done()
        cls.artifact_final.invalidate_cache()
        cls.artifact_final.with_user(cls.admin).action_restart()
        cls.artifact_final.invalidate_cache()
        cls.artifact_final.with_user(cls.admin).action_confirm()
        cls.artifact_final.invalidate_cache()
        cls.artifact_final.with_user(cls.admin).action_approve_approval()
        cls.artifact_final.invalidate_cache()

    @classmethod
    def _create_open_artifact(cls, activity_name):
        """Create a complete artifact and start its curation.

        ``user_id`` is set explicitly to ``base.user_admin`` because
        ``cls.env`` runs as SUPERUSER and the internal user record
        rule would otherwise hide the record from the tour session.
        The caches are invalidated between the transitions because the
        policy fields are cached while the record is still a draft.

        :param activity_name: unique activity name used as the row
            marker by the tour.
        :return: the ``school_learning_artifact`` record On Progress.
        """
        artifact = cls.env["school_learning_artifact"].create(
            {
                "school_id": cls.school.id,
                "academic_year_id": cls.year.id,
                "grade_class_id": cls.grade_class.id,
                "activity_name": activity_name,
                "media_type": "photo",
                "user_id": cls.admin.id,
                "student_ids": [(6, 0, cls.student.ids)],
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

    def test_curate(self):
        """Run the curate tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/06-curate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_curate",
            login="admin",
        )

    def test_reopen(self):
        """Run the reopen tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/07-reopen.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_reopen",
            login="admin",
        )

    def test_set_final_status(self):
        """Run the set final status tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/12-set-final-status.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_set_final_status",
            login="admin",
        )
