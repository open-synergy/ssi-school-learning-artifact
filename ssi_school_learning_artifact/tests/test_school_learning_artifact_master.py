# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactMaster(YamlTransactionCase):
    """Test the master data of the Learning Artifact module.

    Runs the YAML scenarios covering create, write and archive of the
    learning area, category, dimension, phase and graduate profile
    masters, and the distinctive program with its components,
    including the deletion of the components with their program.
    """

    def test_school_learning_artifact_master(self):
        """Run every master data scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_master.yaml")
