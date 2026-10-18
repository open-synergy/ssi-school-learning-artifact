# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactCuration(YamlTransactionCase):
    """Test the rubric based curation of the Learning Artifact.

    Runs the YAML scenarios covering the curation status, ethics
    reason and rubric masters, the rubric chosen per school, the score
    rows created on approval, the total and status computation with
    the knockout and ethics outcomes, the Done gate with the assessor
    rules, and the reopening limited by category and revision count.
    """

    def test_school_learning_artifact_curation(self):
        """Run every curation scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_curation.yaml")
