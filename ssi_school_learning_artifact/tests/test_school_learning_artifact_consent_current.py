# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactConsentCurrent(YamlTransactionCase):
    """Test the current marker of the data privacy consents.

    Runs the YAML scenarios covering which consent applies per contact,
    school and usage, the equality with the consent state of an artifact,
    the search on the marker and the immutability of the log.
    """

    def test_school_learning_artifact_consent_current(self):
        """Run every current consent scenario defined in the YAML file.

        :return: None
        """
        self.run_yaml_scenario(
            "test_data_school_learning_artifact_consent_current.yaml"
        )
