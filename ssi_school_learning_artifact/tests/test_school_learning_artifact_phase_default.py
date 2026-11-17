# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactPhaseDefault(YamlTransactionCase):
    """Test the default phase of the Learning Artifact.

    Runs the YAML scenarios covering the phase filled in when exactly
    one phase matches the school and class, the empty phase when none
    or several match, the manual choice kept until the school or class
    changes, and the submit gate when no phase is chosen.
    """

    def test_school_learning_artifact_phase_default(self):
        """Run every phase default scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_phase_default.yaml")
