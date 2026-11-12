# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.6.0 -> 14.0.1.7.0
#
# Changes: the showcase stage of an artifact became a stored computed
#          field that is emptied when the parental consent no longer
#          allows the showcase or the ethics gate no longer passes.
#          Odoo does not recompute a stored field that already has a
#          column, so the artifacts that sit on the board with a
#          consent that does not allow the showcase would keep their
#          stage. This script recomputes the stage of every artifact
#          that has one, after recomputing the consent flags it
#          depends on (the limited inventory consent now needs a
#          review).
#
# This is a "post" script because the new compute methods must
# already be loaded in the registry.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

MODEL = "school_learning_artifact"


def _recompute_showcase_stage(env):
    """Recompute the showcase stage of the artifacts on the board.

    The consent flags are recomputed first, then the stage, so the
    stage sees the new flags. The model ``write()`` is not called, so
    no guard of the artifact fires.

    :param env: the migration environment
    :return: nothing; recomputes stored fields
    """
    artifacts = (
        env[MODEL]
        .with_context(active_test=False)
        .search([("showcase_stage_id", "!=", False)])
    )
    before = len(artifacts)
    field_names = ["consent_review_required", "showcase_consent_ok"]
    for field_name in field_names:
        env.add_to_compute(artifacts._fields[field_name], artifacts)
    artifacts.flush(field_names)
    env.add_to_compute(artifacts._fields["showcase_stage_id"], artifacts)
    artifacts.flush(["showcase_stage_id"])
    left = len(artifacts.filtered("showcase_stage_id"))
    _logger.info(
        "Recomputed the showcase stage of %s artifact(s); %s left the board.",
        before,
        before - left,
    )


@openupgrade.migrate()
def migrate(env, version):
    """Take the artifacts that do not qualify off the showcase board.

    Recomputes the showcase stage of every artifact that has one. A
    second run changes nothing.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; recomputes stored fields
    """
    _recompute_showcase_stage(env)
