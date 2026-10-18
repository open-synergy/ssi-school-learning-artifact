# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifact(HttpSavepointCase):
    """Tour test for the operating unit work instruction of the artifact."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition fixtures of the create tour.

        One operating unit is linked to a school together with the
        grade type, class and academic year the tour selects. The tour
        session is ``admin``, a manager of operating units who sees
        every operating unit and the field Operating Unit.
        """
        super().setUpClass()
        partner = cls.env["res.partner"].create({"name": "TOUR OU Unit Partner"})
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR OU Unit",
                "code": "TOUROUUN",
                "company_id": cls.env.ref("base.main_company").id,
                "partner_id": partner.id,
            }
        )
        grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR OU Grade Type",
                "code": "TOUROUGT",
                "sequence": 10,
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR OU School",
                "code": "TOUROUSC",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, cls.operating_unit.ids)],
            }
        )
        grade = cls.env["school_grade"].create(
            {
                "name": "TOUR OU Grade",
                "code": "TOUROUGR",
                "sequence": 10,
                "type_id": grade_type.id,
            }
        )
        cls.env["school_grade_class"].create(
            {
                "name": "TOUR OU Class",
                "code": "TOUROUCL",
                "school_id": cls.school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        cls.env["school_academic_year"].create(
            {
                "name": "TOUR OU Year",
                "code": "TOUROUAY",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_learning_artifact``.

        IK: docs/school_learning_artifact/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_operating_unit_"
            "school_learning_artifact_create",
            login="admin",
        )
