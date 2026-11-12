# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_school_learning_artifact"
XMLID_NAME = "school_learning_artifact_view_form_showcase"
MIGRATION_PATH = os.path.join(
    "migrations",
    "14.0.1.11.1",
    "pre-migration.py",
)
OLD_ARCH = (
    "<data><field name='channel_id' position='attributes'>"
    "<attribute name='domain'>[('school_ids', '=', False)]"
    "</attribute></field></data>"
)


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactViewMigration(YamlTransactionCase):
    """Test the old showcase view removal of the 14.0.1.11.1 upgrade.

    Covers the migration script, which YAML scenarios cannot load from
    its file.
    """

    def _load_script(self):
        """Load the pre-migration script from its file.

        :return: the loaded module
        """
        path = os.path.join(get_module_path(MODULE), MIGRATION_PATH)
        spec = importlib.util.spec_from_file_location("pre_migration_1_11_1", path)
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def _view_rows(self):
        """Count the view row and the XML id row of the showcase view.

        :return: tuple of the count of view rows and XML id rows
        """
        cr = self.env.cr
        cr.execute(
            "SELECT res_id FROM ir_model_data "
            "WHERE module = %s AND name = %s AND model = 'ir.ui.view'",
            (MODULE, XMLID_NAME),
        )
        xmlids = cr.fetchall()
        views = 0
        if xmlids:
            cr.execute("SELECT id FROM ir_ui_view WHERE id = %s", (xmlids[0][0],))
            views = len(cr.fetchall())
        return views, len(xmlids)

    def test_delete_old_showcase_view(self):
        """Delete the old inherited showcase view and its XML id.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.11.1/pre-migration.py``, which
        ``EVAL:`` cannot do). The old arch with the removed
        ``school_ids`` domain is planted by SQL, because ORM ``write``
        validates the arch and refuses it. After the script the view
        row and the XML id row are gone, and a second run changes
        nothing.
        """
        view = self.env.ref("%s.%s" % (MODULE, XMLID_NAME))
        self.env.cr.execute(
            "UPDATE ir_ui_view SET arch_db = %s WHERE id = %s",
            (OLD_ARCH, view.id),
        )
        self.env.cache.invalidate()
        self.assertEqual(self._view_rows(), (1, 1))
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.5.1")
        self.assertEqual(self._view_rows(), (0, 0))
        script.migrate(self.env.cr, "14.0.1.5.1")
        self.assertEqual(self._view_rows(), (0, 0))

    def test_missing_showcase_view(self):
        """Raise nothing when the view and its XML id are already gone.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.11.1/pre-migration.py``). The view
        is deleted by SQL first, then the script runs on a database
        without it.
        """
        view = self.env.ref("%s.%s" % (MODULE, XMLID_NAME))
        self.env.cr.execute("DELETE FROM ir_ui_view WHERE id = %s", (view.id,))
        self.env.cr.execute(
            "DELETE FROM ir_model_data WHERE module = %s AND name = %s",
            (MODULE, XMLID_NAME),
        )
        self.env.cache.invalidate()
        self.assertEqual(self._view_rows(), (0, 0))
        script = self._load_script()
        script.migrate(self.env.cr, "14.0.1.5.1")
        self.assertEqual(self._view_rows(), (0, 0))
