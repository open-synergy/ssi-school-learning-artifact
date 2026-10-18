# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactShowcase(YamlTransactionCase):
    """Test the showcase board of the Learning Artifact.

    Runs the YAML scenarios covering the stage and channel masters,
    the word count of the production content, the first stage given
    to a curated artifact, the rules to move into a stage (eligible
    curation status, publication consent, allowed groups), the consent
    policy of the school (minimum consent, limited consent review,
    ignored refusing students, refused assessment consent) and the
    promotion flag.
    """

    def test_school_learning_artifact_showcase(self):
        """Run every showcase scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_showcase.yaml")
