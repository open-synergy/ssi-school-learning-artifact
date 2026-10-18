# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifact(HttpSavepointCase):
    """Tour tests for the ``school_learning_artifact`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create every Pre-Condition fixture required by the 5 tours.

        One shared grade type, school, grade, class, academic year,
        student, learning area and category are created. Each
        state-changing tour then gets its own complete artifact
        (``user_id`` set to ``base.user_admin`` so the tour session
        can see it), moved to the Pre-Condition status of that tour
        through the real action methods.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        # Config Pre-Condition shared by 05-cancel.md: a cancel reason
        # usable on any model.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR LA Cancel Reason",
                "code": "TOUR-LA-CANCEL",
                "global_use": True,
            }
        )

        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR LA Grade Type",
                "code": "TOURLAGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR LA School",
                "code": "TOURLASC",
                "grade_type_id": grade_type.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR LA Grade",
                "code": "TOURLAGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR LA Class",
                "code": "TOURLACL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        cls.year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR LA Year",
                "code": "TOURLAAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR LA Student Contact"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR LA Student",
                "code": "TOURLAST",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.area = cls.env["school_learning_artifact_area"].create(
            {
                "name": "TOUR LA Area",
                "code": "TOURLAAR",
                "school_id": cls.school.id,
                "area_type": "subject",
            }
        )
        cls.category = cls.env["school_learning_artifact_category"].create(
            {
                "name": "TOUR LA Category",
                "code": "TOURLACA",
            }
        )

        # 02-submit.md -- complete Draft record to submit.
        cls.artifact_submit = cls._create_artifact("TOUR LA Submit Activity")

        # 03-withdraw.md -- Waiting for Approval record to withdraw.
        cls.artifact_withdraw = cls._create_artifact("TOUR LA Withdraw Activity")
        cls.artifact_withdraw.with_user(cls.admin).action_confirm()

        # 04-start-curation.md -- Waiting for Approval record to approve.
        cls.artifact_curation = cls._create_artifact("TOUR LA Curation Activity")
        cls.artifact_curation.with_user(cls.admin).action_confirm()

        # 05-cancel.md -- Waiting for Approval record to cancel.
        cls.artifact_cancel = cls._create_artifact("TOUR LA Cancel Activity")
        cls.artifact_cancel.with_user(cls.admin).action_confirm()

    @classmethod
    def _create_artifact(cls, activity_name):
        """Create a complete Draft artifact ready to be submitted.

        ``user_id`` is set explicitly to ``base.user_admin`` because
        ``cls.env`` runs as SUPERUSER and the internal user record
        rule would otherwise hide the record from the tour session.

        :param activity_name: unique activity name used as the row
            marker by the tour.
        :return: the created ``school_learning_artifact`` record.
        """
        return cls.env["school_learning_artifact"].create(
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

    def test_create(self):
        """Run the create tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_create",
            login="admin",
        )

    def test_submit(self):
        """Run the submit tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/02-submit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_submit",
            login="admin",
        )

    def test_withdraw(self):
        """Run the withdraw tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/03-withdraw.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_withdraw",
            login="admin",
        )

    def test_start_curation(self):
        """Run the start curation tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/04-start-curation.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_" "start_curation",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/05-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_cancel",
            login="admin",
        )
