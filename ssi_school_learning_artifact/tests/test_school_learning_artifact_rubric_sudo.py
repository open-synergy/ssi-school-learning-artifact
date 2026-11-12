# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactRubricSudo(YamlTransactionCase):
    """Test that the curation reads the rubric and statuses as sudo.

    Runs the YAML scenario where the responsible user cannot read any
    rubric or curation status, yet reads the revision limit of the
    artifact and finishes the curation without an access error.
    """

    def test_school_learning_artifact_rubric_sudo(self):
        """Run the rubric sudo scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_rubric_sudo.yaml")
