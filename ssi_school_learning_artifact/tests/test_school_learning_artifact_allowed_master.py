# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactAllowedMaster(YamlTransactionCase):
    """Test the allowed master choices of the Learning Artifact.

    Runs the YAML scenarios proving that the category, curation
    status, showcase stage and showcase channel choices hold every
    master record, because the core does not restrict them, and are
    empty when the artifact has no school.
    """

    def test_school_learning_artifact_allowed_master(self):
        """Run every allowed master scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_allowed_master.yaml")
