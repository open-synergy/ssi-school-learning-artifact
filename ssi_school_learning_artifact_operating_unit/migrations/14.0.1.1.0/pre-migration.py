# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.0.2 -> 14.0.1.1.0
#
# Changes: the showcase stage and channel are no longer limited by
#          the grouped record rules (operating unit and company) but
#          by one global rule per master, like the other masters.
#          Odoo does not delete the ir.rule records of a rule file
#          that is rewritten under other ids, so the four old rules
#          are deleted here, before the module data is loaded.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODULE = "ssi_school_learning_artifact_operating_unit"
OLD_RULES = [
    "school_learning_artifact_showcase_stage_operating_unit_rule",
    "school_learning_artifact_showcase_stage_company_rule",
    "school_learning_artifact_showcase_channel_operating_unit_rule",
    "school_learning_artifact_showcase_channel_company_rule",
]


@openupgrade.migrate()
def migrate(env, version):
    """Delete the four grouped record rules of the showcase masters.

    A second run changes nothing: only the rules that still exist
    are deleted.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes records
    """
    existing = [
        "%s.%s" % (MODULE, name)
        for name in OLD_RULES
        if env.ref("%s.%s" % (MODULE, name), raise_if_not_found=False)
    ]
    if existing:
        openupgrade.delete_records_safely_by_xml_id(env, existing)
    _logger.info("Deleted %s old showcase record rule(s).", len(existing))
