# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolDistinctiveProgram(HttpSavepointCase):
    """Tour tests for the ``school_distinctive_program`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the Pre-Condition data of the create tour.

        The branch that owns the program.
        """
        super().setUpClass()
        cls.env["school_branch"].create(
            {
                "name": "TOUR LA Program Branch",
                "code": "TOURLAPB",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_distinctive_program``.

        IK: docs/school_distinctive_program/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_distinctive_program_create",
            login="admin",
        )
