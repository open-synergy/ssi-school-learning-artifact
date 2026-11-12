# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.osv import expression

from .school_learning_artifact_operating_unit_mixin import (
    derive_operating_unit_from_school_vals,
)


class SchoolLearningArtifact(models.Model):
    _name = "school_learning_artifact"
    _inherit = [
        "school_learning_artifact",
        "mixin.single_operating_unit",
    ]

    # Adds the operating unit of the artifact, derived from the school.

    @api.model_create_multi
    def create(self, vals_list):
        """Derive ``operating_unit_id`` from ``school_id`` on create.

        An artifact never creates another document, so there is no
        operating unit to propagate to a derived document.

        :param vals_list: list of value dictionaries
        :return: the created recordset
        """
        for vals in vals_list:
            derive_operating_unit_from_school_vals(self.env, vals)
        return super().create(vals_list)

    def write(self, vals):
        """Re-derive ``operating_unit_id`` when ``school_id`` changes.

        :param vals: values to write
        :return: True
        """
        derive_operating_unit_from_school_vals(self.env, vals)
        return super().write(vals)

    @api.onchange("school_id")
    def onchange_operating_unit_id(self):
        """Set ``operating_unit_id`` from the selected school.

        Mirrors the ``create``/``write`` derivation: a value is only
        set when the school has exactly one operating unit.
        """
        if self.school_id and len(self.school_id.operating_unit_ids) == 1:
            self.operating_unit_id = self.school_id.operating_unit_ids

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_dimension_ids(self):
        """Recompute the allowed dimensions when the unit changes."""
        super()._compute_allowed_dimension_ids()

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_phase_ids(self):
        """Recompute the allowed phases when the unit changes."""
        super()._compute_allowed_phase_ids()

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_category_ids(self):
        """Recompute the allowed categories when the unit changes."""
        super()._compute_allowed_category_ids()

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_curation_status_ids(self):
        """Recompute the allowed statuses when the unit changes."""
        super()._compute_allowed_curation_status_ids()

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_showcase_stage_ids(self):
        """Recompute the allowed stages when the unit changes."""
        super()._compute_allowed_showcase_stage_ids()

    @api.depends("school_id", "operating_unit_id")
    def _compute_allowed_showcase_channel_ids(self):
        """Recompute the allowed channels when the unit changes."""
        super()._compute_allowed_showcase_channel_ids()

    def _get_allowed_school_criteria(self):
        """Narrow the master data choice to the operating unit.

        A master data record applies when it has no operating unit or
        lists the operating unit of the artifact. An artifact without
        operating unit only gets the records without operating unit.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        result = super()._get_allowed_school_criteria()
        if self.operating_unit_id:
            ou_criteria = [
                "|",
                ("operating_unit_ids", "=", False),
                ("operating_unit_ids", "in", [self.operating_unit_id.id]),
            ]
        else:
            ou_criteria = [("operating_unit_ids", "=", False)]
        return expression.AND([result, ou_criteria])

    def _get_rubric_tier_domains(self):
        """Build the rubric search domains, best tier first.

        With an operating unit the tiers are: the core school
        criteria with the unit of the artifact, the core school
        criteria without unit, the core fallback with the unit, and
        the core fallback without unit. Without operating unit only
        the rubrics without unit are offered. A rubric of another
        operating unit is never part of a tier.

        :return: list of search domains (each a list of tuples)
        """
        self.ensure_one()
        base = self._get_rubric_criteria()
        fallback = self._get_fallback_rubric_criteria()
        no_unit = [("operating_unit_ids", "=", False)]
        result = []
        if self.operating_unit_id:
            with_unit = [("operating_unit_ids", "in", [self.operating_unit_id.id])]
            result.append(expression.AND([base, with_unit]))
        result.append(expression.AND([base, no_unit]))
        if self.operating_unit_id:
            result.append(expression.AND([fallback, with_unit]))
        result.append(expression.AND([fallback, no_unit]))
        return result

    def _get_applicable_rubric(self):
        """Pick the rubric of the school and operating unit.

        The tiers of ``_get_rubric_tier_domains`` are tried in order
        and the first one that finds an active rubric wins.

        :return: the rubric record, or an empty recordset when none
            applies
        """
        self.ensure_one()
        obj_rubric = self.env["school_learning_artifact_rubric"].sudo()
        result = obj_rubric
        if self.school_id:
            for domain in self._get_rubric_tier_domains():
                result = obj_rubric.search(domain, order="id asc", limit=1)
                if result:
                    break
        return result

    def _get_rubric_tier_rank(self, rubric):
        """Tell the tier a rubric belongs to.

        :param rubric: a rubric record
        :return: index of the first tier the rubric satisfies, or the
            number of tiers when it satisfies none
        """
        self.ensure_one()
        obj_rubric = self.env["school_learning_artifact_rubric"].sudo()
        domains = self._get_rubric_tier_domains()
        for index, domain in enumerate(domains):
            if obj_rubric.search_count(
                expression.AND([domain, [("id", "=", rubric.id)]])
            ):
                return index
        return len(domains)

    def _is_rubric_stale(self):
        """Tell whether the stored rubric no longer applies.

        The stored rubric is stale when it is empty or inactive, or
        when an active rubric of a better tier exists.

        :return: True when the rubric should be picked again
        """
        self.ensure_one()
        rubric = self.rubric_id.sudo()
        result = False
        if not rubric or not rubric.active:
            result = True
        elif self.school_id:
            best = self._get_applicable_rubric()
            result = bool(best) and self._get_rubric_tier_rank(
                rubric
            ) > self._get_rubric_tier_rank(best)
        return result
