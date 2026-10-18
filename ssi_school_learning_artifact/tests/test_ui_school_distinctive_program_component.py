# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolDistinctiveProgramComponent(HttpSavepointCase):
    """Tour tests for the ``school_distinctive_program_component`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition data of the create tour.

        The program the component belongs to.
        """
        super().setUpClass()
        branch = cls.env["school_branch"].create(
            {
                "name": "TOUR LA Component Branch",
                "code": "TOURLACB",
            }
        )
        cls.env["school_distinctive_program"].create(
            {
                "name": "TOUR LA Component Program",
                "code": "TOURLACP",
                "branch_id": branch.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_distinctive_program_component``.

        IK: docs/school_distinctive_program_component/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_distinctive_program_component_create",
            login="admin",
        )
