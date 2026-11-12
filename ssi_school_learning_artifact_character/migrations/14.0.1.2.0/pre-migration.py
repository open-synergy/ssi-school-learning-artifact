# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.1.1 -> 14.0.1.2.0
#
# Changes: the dominant and the secondary character tag (two Many2one
#          columns) and the character indicators (one Many2many table)
#          of the learning artifact are replaced by four Many2many
#          fields. The old columns and the old table are renamed to
#          their legacy names here, so that the post script can read
#          them to fill the new relations.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

ARTIFACT_TABLE = "school_learning_artifact"
OLD_COLUMNS = ["primary_subconstruct_id", "secondary_subconstruct_id"]
OLD_INDICATOR_TABLE = "school_learning_artifact_character_indicator_rel"


@openupgrade.migrate()
def migrate(env, version):
    """Rename the old character columns and table to legacy names.

    A column or a table that does not exist, or that was already
    renamed, is skipped, so a second run changes nothing.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; renames two columns and one table
    """
    cr = env.cr
    columns = []
    for column in OLD_COLUMNS:
        legacy = openupgrade.get_legacy_name(column)
        if openupgrade.column_exists(
            cr, ARTIFACT_TABLE, column
        ) and not openupgrade.column_exists(cr, ARTIFACT_TABLE, legacy):
            columns.append((column, legacy))
    if columns:
        openupgrade.rename_columns(cr, {ARTIFACT_TABLE: columns})
    tables = []
    legacy_table = openupgrade.get_legacy_name(OLD_INDICATOR_TABLE)
    if openupgrade.table_exists(cr, OLD_INDICATOR_TABLE) and not (
        openupgrade.table_exists(cr, legacy_table)
    ):
        tables.append((OLD_INDICATOR_TABLE, legacy_table))
    if tables:
        openupgrade.rename_tables(cr, tables)
    _logger.info(
        "Renamed %s column(s) and %s table(s) to legacy names.",
        len(columns),
        len(tables),
    )
