# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolLearningArtifactShowcaseChannel(HttpSavepointCase):
    """Tour tests for the showcase channel work instructions."""

    def test_create(self):
        """Run the create tour for the showcase channel master.

        IK: docs/school_learning_artifact_showcase_channel/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_learning_artifact_school_learning_artifact_"
            "showcase_channel_create",
            login="admin",
        )
