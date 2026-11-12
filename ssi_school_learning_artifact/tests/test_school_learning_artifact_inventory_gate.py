# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactInventoryGate(YamlTransactionCase):
    """Test the ethics gate aspect filled from the inventory consent.

    Runs the YAML scenarios covering the gate row filled by the
    system, its write lock, the limited consent review, the recompute
    of the gate and of the showcase board when a consent changes, and
    the rules of the gate source on a rubric aspect.
    """

    def test_school_learning_artifact_inventory_gate(self):
        """Run every inventory gate scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_inventory_gate.yaml")
