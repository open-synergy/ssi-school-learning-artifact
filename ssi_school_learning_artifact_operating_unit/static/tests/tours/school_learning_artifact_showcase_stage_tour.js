// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact_operating_unit.school_learning_artifact_showcase_stage_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_learning_artifact_showcase_stage/01-create.md
        tour.register(
            "ssi_school_learning_artifact_operating_unit_school_learning_artifact_showcase_stage_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Base Flow 1 -- Open the Showcase Stages menu. "Learning Artifact"
                // is a level-3 grouping menu rendered as a non-clickable
                // header, so there is no step for it.
                [
                    tour.stepUtils.showAppsMenuItem(),
                    {
                        content: "Open the School app",
                        trigger:
                            '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                    },
                    {
                        content: "Open the Configuration menu",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                    },
                    {
                        content: "Open the Showcase Stages menu",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_school_learning_artifact.school_learning_artifact_showcase_stage_menu"]',
                    },
                    {
                        content: "Showcase Stage list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(Learning Artifact Showcase Stages)",
                        extra_trigger: ".o_list_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // Base Flow 2 -- Click the New button. (14.0: "Create")
                    {
                        content: "Click New",
                        trigger: ".o_list_button_add",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open in edit mode",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // Base Flow 3 -- Fill in the required fields.
                    {
                        content: "Fill in the name",
                        trigger: ".o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR OUM Showcase Stage Create",
                    },
                    {
                        content: "Fill in the code",
                        trigger: ".o_field_widget[name='code']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOURSHSOU01",
                    },
                    // Delta Flow 1 -- Check the Operating Unit field.
                    {
                        content: "Operating Unit field is displayed",
                        trigger: ".o_field_widget[name='operating_unit_ids'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // Delta Flow 2 -- Select the operating unit.
                    {
                        content: "Type the operating unit",
                        trigger: ".o_field_widget[name='operating_unit_ids'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR OUM Unit",
                    },
                    {
                        content: "Pick the operating unit from the dropdown",
                        trigger:
                            ".ui-autocomplete .ui-menu-item a:contains(TOUR OUM Unit)",
                        in_modal: false,
                    },
                    // Base Flow 4 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                    // Delta Post-Condition -- the saved form shows the unit.
                    {
                        content: "Record is saved",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(TOUR OUM Showcase Stage Create)",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Operating Unit is displayed",
                        trigger:
                            ".o_field_widget[name='operating_unit_ids']:contains(TOUR OUM Unit)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
