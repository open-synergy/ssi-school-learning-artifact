# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Test the operating unit of the Learning Artifact.

    Covers the derivation of ``operating_unit_id`` from ``school_id``
    on create, write and onchange, and the record rule that limits the
    users of the Operating Unit group to the artifacts of their own
    operating units.
    """

    def test_derivation(self):
        """Run every operating unit derivation scenario.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_derivation.yaml")

    def test_visibility(self):
        """Run every operating unit visibility scenario.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_visibility.yaml")
