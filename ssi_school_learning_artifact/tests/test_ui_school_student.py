# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolStudent(HttpSavepointCase):
    """Tour tests for the ``school_student`` consent work instruction."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the consent tour.

        One school, student, privacy notice and one purpose that is
        mapped to the publication usage are created.
        """
        super().setUpClass()
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR LC Grade Type",
                "code": "TOURLCGT",
                "sequence": 10,
            }
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR LC School",
                "code": "TOURLCSC",
                "grade_type_id": grade_type.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR LC Student Contact"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR LC Student",
                "code": "TOURLCST",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        cls.notice = cls.env["partner_consent_notice"].create(
            {
                "name": "TOUR LC Notice",
                "code": "TOURLCNO",
                "version": "1.0",
                "body": "Privacy notice text",
            }
        )
        cls.purpose = cls.env["partner_consent_purpose"].create(
            {
                "name": "TOUR LC Publication Purpose",
                "code": "TOURLCPU",
                "learning_artifact_usage": "publication",
            }
        )

    def test_record_learning_artifact_consent(self):
        """Run the record consent tour for ``school_student``.

        IK: docs/school_student/01-record-learning-artifact-consent.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_student_record_learning_artifact_consent",
            login="admin",
        )
