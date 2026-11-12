# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_school_learning_artifact_operating_unit"
MIGRATION_DIR = os.path.join("migrations", "14.0.1.1.0")
MASTER_MODELS = [
    "school_learning_artifact_category",
    "school_learning_artifact_phase",
    "school_learning_artifact_dimension",
    "school_learning_artifact_curation_status",
    "school_learning_artifact_showcase_stage",
    "school_learning_artifact_showcase_channel",
]


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactOperatingUnitMigration(YamlTransactionCase):
    """Test the operating unit migration of the 14.0.1.1.0 upgrade.

    Covers the post-migration script, which YAML scenarios cannot load
    from its file.
    """

    def setUp(self):
        """Create the operating units and the schools of the tests.

        :return: None
        """
        super().setUp()
        env = self.env
        self.unit_a = self._create_unit("MIGA")
        self.unit_b = self._create_unit("MIGB")
        grade_type = env["school_grade_type"].create(
            {"name": "OUM Grade Type", "code": "/", "sequence": 10}
        )
        self.school_a = env["school"].create(
            {
                "name": "OUM School A",
                "code": "/",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, self.unit_a.ids)],
            }
        )
        self.school_ab = env["school"].create(
            {
                "name": "OUM School AB",
                "code": "/",
                "grade_type_id": grade_type.id,
                "operating_unit_ids": [(6, 0, (self.unit_a | self.unit_b).ids)],
            }
        )

    def _create_unit(self, code):
        """Create an operating unit with its partner.

        :param code: code of the operating unit
        :return: the operating unit record
        """
        env = self.env
        partner = env["res.partner"].create({"name": "OUM %s" % code})
        return env["operating.unit"].create(
            {
                "name": "OUM %s" % code,
                "code": code,
                "company_id": env.ref("base.main_company").id,
                "partner_id": partner.id,
            }
        )

    def _load_script(self, name):
        """Load a migration script from its file.

        :param name: file name inside the migration directory
        :return: the loaded module
        """
        path = os.path.join(get_module_path(MODULE), MIGRATION_DIR, name)
        spec = importlib.util.spec_from_file_location("oum_%s" % name[:3], path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def test_fill_operating_units(self):
        """Fill the unit of each master from the units of its schools.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.1.0/post-migration.py``, which
        YAML cannot do). A master of school A gets unit A, a master of
        schools A and AB gets both units, a master without school stays
        without unit, and a second run changes nothing.
        """
        env = self.env
        cases = {}
        for model_name in MASTER_MODELS:
            values = {"name": "OUM %s" % model_name, "code": "/"}
            if model_name.endswith("showcase_stage"):
                values["sequence"] = 10
            if model_name.endswith("curation_status"):
                values["category"] = "eligible"
            only_a = env[model_name].create(
                dict(values, school_ids=[(6, 0, self.school_a.ids)])
            )
            both = env[model_name].create(
                dict(values, school_ids=[(6, 0, self.school_ab.ids)])
            )
            none = env[model_name].create(values)
            (only_a | both | none).write({"operating_unit_ids": [(5, 0, 0)]})
            cases[model_name] = (only_a, both, none)
        env["school_learning_artifact_category"].flush()
        script = self._load_script("post-migration.py")
        for _round in range(2):
            script.migrate(env.cr, "14.0.1.0.2")
            env.cache.invalidate()
            for only_a, both, none in cases.values():
                self.assertEqual(only_a.operating_unit_ids, self.unit_a)
                self.assertEqual(both.operating_unit_ids, self.unit_a | self.unit_b)
                self.assertFalse(none.operating_unit_ids)

    def test_pre_migration_runs_without_old_rules(self):
        """Run the pre-migration script when the old rules are absent.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file). A fresh install has none of the four old rules, so
        the script must leave the rules of the module untouched.
        """
        rule = self.env.ref(
            "ssi_school_learning_artifact_operating_unit."
            "school_learning_artifact_showcase_stage_rule_ou"
        )
        script = self._load_script("pre-migration.py")
        script.migrate(self.env.cr, "14.0.1.0.2")
        self.assertTrue(rule.exists())
