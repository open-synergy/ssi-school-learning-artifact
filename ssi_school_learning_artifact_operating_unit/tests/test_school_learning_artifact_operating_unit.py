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
    on create, write and onchange, the record rule that limits the
    users of the Operating Unit group to the artifacts of their own
    operating units, the global record rules that limit every user to
    the master data of the own operating units, and the choices of
    the artifact that follow its operating unit.
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

    def test_showcase_scope(self):
        """Run every master data scope scenario.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_showcase_scope.yaml")

    def test_allowed_ou(self):
        """Run every master choice scenario of the artifact unit.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_allowed_ou.yaml")
