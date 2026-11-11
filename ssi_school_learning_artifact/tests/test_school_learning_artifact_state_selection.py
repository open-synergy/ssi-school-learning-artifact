# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactStateSelection(YamlTransactionCase):
    """Test the ownership of the artifact state selection values.

    Runs the YAML scenario proving that all six state values have an
    xmlid owned by this module, with the expected label and order.
    """

    def test_school_learning_artifact_state_selection(self):
        """Run the state selection ownership scenario.

        :return: None
        """
        self.run_yaml_scenario(
            "test_data_school_learning_artifact_state_selection.yaml"
        )
