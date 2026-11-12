# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.11.0 -> 14.0.1.11.1
#
# Changes: none in the code of the module. The upgrade of a database
#          that still has the old showcase inherited form view (from
#          14.0.1.5.1 for example) stops with a ParseError: the manifest
#          loads ``views/school_learning_artifact.xml`` before
#          ``views/school_learning_artifact_showcase.xml``, so the
#          validation of the main form merges the old inherited view
#          stored in the database, whose arch still has a domain on the
#          removed field ``school_ids`` of the showcase channel.
#
# This is a "pre" script on purpose: it is the only phase that runs
# before the view files are loaded. It deletes the inherited view and
# its XML id; the showcase view file then creates both again with the
# current arch.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODULE = "ssi_school_learning_artifact"
XMLID_NAME = "school_learning_artifact_view_form_showcase"


@openupgrade.migrate()
def migrate(env, version):
    """Delete the old showcase inherited form view and its XML id.

    A second run, or a run when the XML id does not exist, changes
    nothing.

    :param env: the migration environment
    :param version: the version being migrated from (unused)
    :return: nothing; deletes the view, its translations and its XML id
    """
    cr = env.cr
    cr.execute(
        "SELECT res_id FROM ir_model_data "
        "WHERE module = %s AND name = %s AND model = 'ir.ui.view'",
        (MODULE, XMLID_NAME),
    )
    row = cr.fetchone()
    if not row:
        _logger.info("The old showcase view %s is not found.", XMLID_NAME)
        return
    view_id = row[0]
    openupgrade.logged_query(
        cr,
        "DELETE FROM ir_translation WHERE name LIKE 'ir.ui.view,%%' " "AND res_id = %s",
        (view_id,),
    )
    openupgrade.logged_query(
        cr,
        "DELETE FROM ir_ui_view WHERE id = %s",
        (view_id,),
    )
    openupgrade.logged_query(
        cr,
        "DELETE FROM ir_model_data WHERE module = %s AND name = %s "
        "AND model = 'ir.ui.view'",
        (MODULE, XMLID_NAME),
    )
    _logger.info("Deleted the old showcase view %s.", XMLID_NAME)
