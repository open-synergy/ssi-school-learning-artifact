# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactCharacter(YamlTransactionCase):
    """Test the character tag of the Learning Artifact.

    Runs the YAML scenarios covering the status of an indicator per
    grade type, the choice of character tags filtered by the grade type
    of the artifact, the rule on the not clearly evident mark, the
    freedom to tag an artifact whose assessment consent is refused and
    the policy that allows to fill in the tags.
    """

    def test_school_learning_artifact_character(self):
        """Run every character tag scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact_character.yaml")
