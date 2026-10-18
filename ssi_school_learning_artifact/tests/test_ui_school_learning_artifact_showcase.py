# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactShowcase(HttpSavepointCase):
    """Tour tests for the showcase work instructions of the artifact."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 3 tours.

        One school with a rubric of a single aspect that makes a score
        of 3 eligible, an initial and a selectable showcase stage, and a
        showcase channel are created. Three curated artifacts are built
        through the real action methods, one per tour. The review
        artifact belongs to a student with a limited publication
        consent, and the school treats a limited consent as a review
        task. ``user_id`` is set to ``base.user_admin`` so the tour
        session can see the artifacts.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR SH Grade Type",
                "code": "TOURSHGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR SH School",
                "code": "TOURSHSC",
                "grade_type_id": grade_type.id,
                "showcase_limited_treatment": "review",
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR SH Grade",
                "code": "TOURSHGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR SH Class",
                "code": "TOURSHCL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR SH Year",
                "code": "TOURSHAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.contact = cls.env["res.partner"].create({"name": "TOUR SH Student Contact"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR SH Student",
                "code": "TOURSHST",
                "contact_id": cls.contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR SH Area",
                "code": "TOURSHAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        cls.category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR SH Category",
                "code": "TOURSHCA",
            }
        )
        obj_status = cls.env["school_learning_artifact_curation_status"]
        eligible = obj_status.create(
            {
                "name": "TOUR SH Eligible",
                "code": "TOURSHEL",
                "category": "eligible",
            }
        )
        rejected = obj_status.create(
            {
                "name": "TOUR SH Rejected",
                "code": "TOURSHRJ",
                "category": "rejected",
            }
        )
        cls.env["school_learning_artifact_rubric"].create(
            {
                "name": "TOUR SH Rubric",
                "code": "TOURSHRB",
                "school_ids": [(6, 0, cls.school.ids)],
                "ethics_fail_status_id": rejected.id,
                "criterion_ids": [
                    (0, 0, {"code": "TA1", "name": "TOUR SH Aspect"}),
                ],
                "threshold_ids": [
                    (0, 0, {"min_total": 3, "status_id": eligible.id}),
                ],
            }
        )
        obj_stage = cls.env["school_learning_artifact_showcase_stage"]
        obj_stage.create(
            {
                "name": "TOUR SH Initial",
                "code": "TOURSHS1",
                "sequence": 1,
                "school_ids": [(6, 0, cls.school.ids)],
            }
        )
        obj_stage.create(
            {
                "name": "TOUR SH Selected",
                "code": "TOURSHS2",
                "sequence": 2,
                "school_ids": [(6, 0, cls.school.ids)],
            }
        )
        cls.env["school_learning_artifact_showcase_channel"].create(
            {
                "name": "TOUR SH Channel",
                "code": "TOURSHCH",
                "school_ids": [(6, 0, cls.school.ids)],
            }
        )
        notice = cls.env["partner_consent_notice"].create(
            {
                "name": "TOUR SH Notice",
                "code": "TOURSHNT",
                "version": "1.0",
                "body": "Privacy notice text",
            }
        )
        purpose = cls.env["partner_consent_purpose"].create(
            {
                "name": "TOUR SH Publication Purpose",
                "code": "TOURSHPP",
                "learning_artifact_usage": "publication",
            }
        )
        cls.env["res.partner.consent"].create(
            {
                "partner_id": cls.contact.id,
                "school_id": cls.school.id,
                "notice_id": notice.id,
                "purpose_id": purpose.id,
                "consent_type": "grant",
                "consent_level": "limited",
                "consent_date": "2026-10-01 08:00:00",
                "channel": "manual",
            }
        )

        # 08-select-for-showcase.md -- curated record to move.
        cls.artifact_select = cls._create_curated_artifact("TOUR SH Select Activity")
        # 09-produce-showcase.md -- curated record to produce for.
        cls.artifact_produce = cls._create_curated_artifact("TOUR SH Produce Activity")
        # 10-review-limited-consent.md -- curated, limited consent.
        cls.artifact_review = cls._create_curated_artifact("TOUR SH Review Activity")

    @classmethod
    def _create_curated_artifact(cls, activity_name):
        """Create an artifact and move it to Curated.

        ``user_id`` is set explicitly to ``base.user_admin`` because
        ``cls.env`` runs as SUPERUSER and the internal user record
        rule would otherwise hide the record from the tour session.
        The caches are invalidated between the transitions because the
        policy fields are cached while the record is still a draft.

        :param activity_name: unique activity name used as the row
            marker by the tour.
        :return: the ``school_learning_artifact`` record Curated.
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
        artifact.write({"ethics_result": "pass"})
        artifact.score_ids.write({"score": 3})
        artifact.invalidate_cache()
        artifact.with_user(cls.admin).action_done()
        artifact.invalidate_cache()
        return artifact

    def test_select_for_showcase(self):
        """Run the select tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/08-select-for-showcase.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "select_for_showcase",
            login="admin",
        )

    def test_produce_showcase(self):
        """Run the produce tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/09-produce-showcase.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "produce_showcase",
            login="admin",
        )

    def test_review_limited_consent(self):
        """Run the review tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/10-review-limited-consent.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "review_limited_consent",
            login="admin",
        )
