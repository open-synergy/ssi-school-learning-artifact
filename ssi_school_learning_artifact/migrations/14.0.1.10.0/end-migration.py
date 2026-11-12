# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.9.3 -> 14.0.1.10.0
#
# Changes: the seven learning artifact masters (category, phase,
#          dimension, rubric, curation status, showcase stage and
#          showcase channel) no longer have the ``school_ids`` field.
#          Their restriction is given by extension modules. Odoo does
#          not drop the relation table of a Many2many field that was
#          removed from the code, so this script drops the seven
#          tables.
#
# This is an "end" script, not "pre" or "post", on purpose: it runs
# after the "post" scripts of every module, so the operating unit
# module can still read the school relation tables to fill its
# operating units, even when one deploy jumps over several versions.
# The field rows are still in ``ir_model_fields`` at this stage, so
# the table names are read from there; the names that the code gave
# explicitly or by default are listed as a safety net.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MASTER_MODELS = [
    "school_learning_artifact_category",
    "school_learning_artifact_phase",
    "school_learning_artifact_dimension",
    "school_learning_artifact_rubric",
    "school_learning_artifact_curation_status",
    "school_learning_artifact_showcase_stage",
    "school_learning_artifact_showcase_channel",
]

# Names given in the code (rubric, status, stage, channel) or derived by
# Odoo from the two table names (category, phase, dimension).
KNOWN_TABLES = [
    "school_school_learning_artifact_category_rel",
    "school_school_learning_artifact_phase_rel",
    "school_school_learning_artifact_dimension_rel",
    "school_la_rubric_school_rel",
    "school_la_curation_status_school_rel",
    "school_la_showcase_stage_school_rel",
    "school_la_showcase_channel_school_rel",
]


def _get_relation_tables(cr):
    """Collect the names of the school relation tables to drop.

    :param cr: database cursor
    :return: sorted list of table names, from the registry rows of the
        ``school_ids`` fields plus the known names
    """
    cr.execute(
        "SELECT relation_table FROM ir_model_fields "
        "WHERE name = 'school_ids' AND model IN %s "
        "AND relation_table IS NOT NULL",
        (tuple(MASTER_MODELS),),
    )
    result = {row[0] for row in cr.fetchall()}
    result.update(KNOWN_TABLES)
    return sorted(result)


@openupgrade.migrate()
def migrate(env, version):
    """Drop the school relation tables of the seven masters.

    A second run changes nothing: ``DROP TABLE IF EXISTS`` skips the
    tables that are already gone.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; drops tables
    """
    cr = env.cr
    for table in _get_relation_tables(cr):
        if openupgrade.table_exists(cr, table):
            openupgrade.logged_query(cr, 'DROP TABLE IF EXISTS "%s"' % table)
            _logger.info("Dropped the school relation table %s.", table)
