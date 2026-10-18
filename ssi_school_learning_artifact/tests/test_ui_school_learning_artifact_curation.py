# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactCuration(HttpSavepointCase):
    """Tour tests for the curation work instructions of the artifact."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 2 tours.

        One school with its own rubric of a single aspect is created,
        with an eligible and a revision status. The curate tour gets
        an artifact that is On Progress. The reopen tour gets an
        artifact that is Curated with the revision category. Both
        move through the real action methods, and ``user_id`` is set
        to ``base.user_admin`` so the tour session can see them.
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
        cls.artifact_reopen.write(
            {
                "ethics_result": "pass",
                "recommendation": "Strengthen the reflection",
            }
        )
        cls.artifact_reopen.score_ids.write({"score": 2})
        cls.artifact_reopen.invalidate_cache()
        cls.artifact_reopen.with_user(cls.admin).action_done()

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
