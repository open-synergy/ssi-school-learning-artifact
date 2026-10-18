# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Learning Artifact - Character Tag",
    "version": "14.0.1.0.1",
    "website": "https://simetri-sinergi.id",
    # pylint: disable=line-too-long
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, Odoo Community Association (OCA)",  # noqa: B950
    # pylint: enable=line-too-long
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_learning_artifact",
        "ssi_school_character",
        "web_tour",
    ],
    "data": [
        "security/ir_model_access/school_character_indicator_grade_status.xml",
        "policy_template/school_learning_artifact.xml",
        "views/school_character_indicator.xml",
        "views/school_learning_artifact.xml",
        "views/assets.xml",
    ],
}
