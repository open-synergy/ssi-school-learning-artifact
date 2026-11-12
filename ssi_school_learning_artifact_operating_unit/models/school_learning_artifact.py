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

    def _get_rubric_criteria(self):
        """Narrow the rubric choice to the operating unit.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        result = super()._get_rubric_criteria()
        if self.operating_unit_id:
            ou_criteria = [("operating_unit_ids", "in", [self.operating_unit_id.id])]
        else:
            ou_criteria = [("operating_unit_ids", "=", False)]
        return expression.AND([result, ou_criteria])

    def _get_fallback_rubric_criteria(self):
        """Narrow the fallback rubric to the rubrics without unit.

        :return: search domain (list of tuples)
        """
        self.ensure_one()
        result = super()._get_fallback_rubric_criteria()
        return expression.AND([result, [("operating_unit_ids", "=", False)]])
