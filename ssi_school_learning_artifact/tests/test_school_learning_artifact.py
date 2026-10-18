# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifact(YamlTransactionCase):
    """Test the Learning Artifact document.

    Runs the YAML scenarios covering the generated code and computed
    fields, the components, dimensions and phases offered per school,
    the description word count, the submit, withdraw, start curation
    and cancel life cycle, and the submit gate that rejects missing
    students, link, prefix mismatch and the fields a school requires.
    """

    def test_school_learning_artifact(self):
        """Run every Learning Artifact scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario("test_data_school_learning_artifact.yaml")
