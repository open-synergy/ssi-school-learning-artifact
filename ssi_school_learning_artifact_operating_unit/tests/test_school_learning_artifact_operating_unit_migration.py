# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os
from unittest import mock

from odoo_yaml_test import YamlTransactionCase
from openupgradelib import openupgrade

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

    def _has_school_relation(self):
        """Tell whether the old school relation still exists.

        :return: True when the core still has ``school_ids`` and its
            relation table
        """
        field = self.env[MASTER_MODELS[0]]._fields.get("school_ids")
        return bool(field) and openupgrade.table_exists(self.env.cr, field.relation)

    def _prepare_cases(self):
        """Create the masters with their schools and clear their units.

        :return: dict of model name to the tuple (master of school A,
            master of schools A and AB, master without school)
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
        return cases

    def _assert_filled(self, cases, skip_model=None):
        """Assert the units of the masters after the migration.

        :param cases: the result of ``_prepare_cases``
        :param skip_model: model whose masters must stay without unit
        :return: None
        """
        self.env.cache.invalidate()
        for model_name, (only_a, both, none) in cases.items():
            if model_name == skip_model:
                self.assertFalse((only_a | both | none).operating_unit_ids)
                continue
            self.assertEqual(only_a.operating_unit_ids, self.unit_a)
            self.assertEqual(both.operating_unit_ids, self.unit_a | self.unit_b)
            self.assertFalse(none.operating_unit_ids)

    def test_fill_operating_units(self):
        """Fill the unit of each master from the units of its schools.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.1.0/post-migration.py``, which
        YAML cannot do). A master of school A gets unit A, a master of
        schools A and AB gets both units, a master without school stays
        without unit, and a second run changes nothing.
        """
        if not self._has_school_relation():
            self.skipTest("The core no longer limits the masters by school.")
        cases = self._prepare_cases()
        script = self._load_script("post-migration.py")
        for _round in range(2):
            script.migrate(self.env.cr, "14.0.1.0.2")
            self._assert_filled(cases)

    def test_fill_operating_units_without_registry_field(self):
        """Fill the units when ``school_ids`` is gone from the registry.

        Pure Python -- trigger P6 (L-15: the field is removed from the
        registry with ``mock.patch.dict``) plus P10 (L-11: the script
        is loaded from its file). This is the upgrade of the glue and
        of the core without ``school_ids`` in one run: the relation
        tables still exist, so the result must be the same as when the
        field is present.
        """
        if not self._has_school_relation():
            self.skipTest("The core no longer limits the masters by school.")
        cases = self._prepare_cases()
        script = self._load_script("post-migration.py")
        patchers = [
            mock.patch.dict(self.env[model_name]._fields)
            for model_name in MASTER_MODELS
        ]
        for patcher in patchers:
            patcher.start()
            self.addCleanup(patcher.stop)
        for model_name in MASTER_MODELS:
            self.env[model_name]._fields.pop("school_ids")
        for _round in range(2):
            script.migrate(self.env.cr, "14.0.1.0.2")
            self._assert_filled(cases)

    def test_fill_operating_units_without_relation_table(self):
        """Skip a master whose school relation table does not exist.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file). The table of the category master is renamed inside
        the test transaction (rolled back afterwards): the script must
        finish without error, leave that master untouched and still
        fill the others. When the core no longer has the relation (a
        fresh install after the school removal) nothing is renamed and
        the script must simply finish without error.
        """
        script = self._load_script("post-migration.py")
        if not self._has_school_relation():
            script.migrate(self.env.cr, "14.0.1.0.2")
            return
        model_name = "school_learning_artifact_category"
        cases = self._prepare_cases()
        table = script._get_school_relation(self.env, model_name)[0]
        self.env.cr.execute('ALTER TABLE "%s" RENAME TO "%s_gone"' % (table, table))
        script.migrate(self.env.cr, "14.0.1.0.2")
        self._assert_filled(cases, skip_model=model_name)

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
