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
# The relation table names come from the registry, not from literals,
# because the Many2many fields were declared without a table name.
# This is a "post" script because the new fields must already be
# loaded in the registry.

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


def _fill_operating_units(env, model_name):
    """Copy the school operating units into one master model.

    :param env: the migration environment
    :param model_name: technical name of the master model
    :return: number of relation rows inserted, 0 when the old school
        relation table is gone
    """
    cr = env.cr
    model = env[model_name]
    school_field = model._fields.get("school_ids")
    ou_field = model._fields.get("operating_unit_ids")
    unit_field = env["school"]._fields.get("operating_unit_ids")
    if not (school_field and ou_field and unit_field):
        return 0
    if not openupgrade.table_exists(cr, school_field.relation):
        return 0
    query = (
        "INSERT INTO {ou_rel} ({ou_master}, {ou_unit}) "
        "SELECT DISTINCT school_rel.{school_master}, unit_rel.{unit_col} "
        "FROM {school_rel} school_rel "
        "JOIN {unit_rel} unit_rel "
        "ON unit_rel.{unit_school} = school_rel.{school_col} "
        "ON CONFLICT DO NOTHING"
    ).format(
        ou_rel=ou_field.relation,
        ou_master=ou_field.column1,
        ou_unit=ou_field.column2,
        school_rel=school_field.relation,
        school_master=school_field.column1,
        school_col=school_field.column2,
        unit_rel=unit_field.relation,
        unit_school=unit_field.column1,
        unit_col=unit_field.column2,
    )
    return openupgrade.logged_query(cr, query)


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
