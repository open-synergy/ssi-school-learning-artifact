# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactCategory(HttpSavepointCase):
    """Tour tests for the ``school_learning_artifact_category`` work instructions."""

    def test_create(self):
        """Run the create tour for ``school_learning_artifact_category``.

        IK: docs/school_learning_artifact_category/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_category_create",
            login="admin",
        )
