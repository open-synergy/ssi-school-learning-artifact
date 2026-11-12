# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.2 -> 14.0.1.1.0
#
# Changes: the seven learning artifact masters are limited by their
#          operating units instead of their schools. This script fills
#          the operating units of each master from the operating units
#          of the schools it listed. A master without school stays
#          without operating unit. The school relation tables are only
#          read: the core module drops them in a later version.
#
# The old school side is read with SQL, not through the registry. The
# ``school_ids`` field may already be gone from the registry when the
# core module is upgraded in the same run, while its relation table
# is only dropped in the ``end`` stage of the core module. The table
# and column names come from ``ir_model_fields`` (the row still exists
# while this script runs) or, as a fallback, from the fixed names the
# core module declared. The operating unit side stays on the registry:
# both fields are always loaded when this "post" script runs.

import logging

from openupgradelib import openupgrade
from psycopg2 import sql

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


# Relation names the core module declared explicitly:
# model name -> (relation table, master column, school column).
FIXED_SCHOOL_RELATIONS = {
    "school_learning_artifact_rubric": (
        "school_la_rubric_school_rel",
        "rubric_id",
        "school_id",
    ),
    "school_learning_artifact_curation_status": (
        "school_la_curation_status_school_rel",
        "status_id",
        "school_id",
    ),
    "school_learning_artifact_showcase_stage": (
        "school_la_showcase_stage_school_rel",
        "stage_id",
        "school_id",
    ),
    "school_learning_artifact_showcase_channel": (
        "school_la_showcase_channel_school_rel",
        "channel_id",
        "school_id",
    ),
}


def _get_school_relation(env, model_name):
    """Find the old school relation table of one master model.

    The reflected ``ir_model_fields`` row is read first. When it is
    missing, the fixed names of the core module are used; the three
    masters without explicit names use the default Odoo naming.

    :param env: the migration environment
    :param model_name: technical name of the master model
    :return: tuple of relation table, master column and school column
    """
    cr = env.cr
    cr.execute(
        "SELECT relation_table, column1, column2 FROM ir_model_fields "
        "WHERE model = %s AND name = 'school_ids' "
        "AND relation_table IS NOT NULL "
        "AND column1 IS NOT NULL AND column2 IS NOT NULL",
        (model_name,),
    )
    row = cr.fetchone()
    if row:
        return tuple(row)
    if model_name in FIXED_SCHOOL_RELATIONS:
        return FIXED_SCHOOL_RELATIONS[model_name]
    table = env[model_name]._table
    return ("school_%s_rel" % table, "%s_id" % table, "school_id")


def _fill_operating_units(env, model_name):
    """Copy the school operating units into one master model.

    :param env: the migration environment
    :param model_name: technical name of the master model
    :return: number of relation rows inserted, 0 when the old school
        relation table is gone
    """
    cr = env.cr
    model = env[model_name]
    ou_field = model._fields.get("operating_unit_ids")
    unit_field = env["school"]._fields.get("operating_unit_ids")
    if not (ou_field and unit_field):
        return 0
    school_rel, school_master, school_col = _get_school_relation(env, model_name)
    if not openupgrade.table_exists(cr, school_rel):
        return 0
    query = sql.SQL(
        "INSERT INTO {ou_rel} ({ou_master}, {ou_unit}) "
        "SELECT DISTINCT school_rel.{school_master}, unit_rel.{unit_col} "
        "FROM {school_rel} school_rel "
        "JOIN {unit_rel} unit_rel "
        "ON unit_rel.{unit_school} = school_rel.{school_col} "
        "ON CONFLICT DO NOTHING"
    ).format(
        ou_rel=sql.Identifier(ou_field.relation),
        ou_master=sql.Identifier(ou_field.column1),
        ou_unit=sql.Identifier(ou_field.column2),
        school_rel=sql.Identifier(school_rel),
        school_master=sql.Identifier(school_master),
        school_col=sql.Identifier(school_col),
        unit_rel=sql.Identifier(unit_field.relation),
        unit_school=sql.Identifier(unit_field.column1),
        unit_col=sql.Identifier(unit_field.column2),
    )
    return openupgrade.logged_query(cr, query.as_string(cr._obj))


@openupgrade.migrate()
def migrate(env, version):
    """Fill the operating units of the masters from their schools.

    A second run changes nothing: the insert skips the pairs that
    already exist.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; inserts relation rows
    """
    for model_name in MASTER_MODELS:
        count = _fill_operating_units(env, model_name)
        _logger.info("Filled %s operating unit link(s) of %s.", count, model_name)
