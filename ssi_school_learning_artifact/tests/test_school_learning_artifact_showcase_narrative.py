# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactShowcaseNarrative(YamlTransactionCase):
    """Test the narrative workflow of the showcase production.

    Runs the YAML scenarios covering the return to the teacher, the
    edit rights while assigned, the word limits of the channel, the
    revision limit of the school, the sequential approval with an
    empty or filled approval template, the rejection and the locks
    on the content and on the ready flag.
    """

    def test_school_learning_artifact_showcase_narrative(self):
        """Run every narrative scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario(
            "test_data_school_learning_artifact_showcase_narrative.yaml"
        )
