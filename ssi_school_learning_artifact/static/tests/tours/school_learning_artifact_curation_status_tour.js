// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact.school_learning_artifact_curation_status_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Flow 1 of the IK: "Open the School > Configuration > Learning
        // Artifact > Curation Statuses menu." "Learning Artifact"
        // (menu_school_learning_artifact_configuration) is a level-3 grouping
        // menuitem without action, rendered by 14.0 as a non-clickable dropdown
        // header without data-menu-xmlid, so there is no step for it.
        function openList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school.menu_school_configuration"]',
                },
                {
                    content: "Open the Curation Statuses menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_learning_artifact.school_learning_artifact_curation_status_menu"]',
                },
                {
                    content: "Learning Artifact Curation Statuses list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Learning Artifact Curation Statuses)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // IK: docs/school_learning_artifact_curation_status/01-create.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_curation_status_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the menu.
                openList(),
                [
                    // Flow 2 -- Click the New button. (14.0: "Create")
                    {
                        content: "Click New",
                        trigger: ".o_list_button_add",
                        extra_trigger: ".o_list_view",
                    },
                    {
                        content: "Form is open in edit mode",
                        trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only; do not trigger the default click action.
                        },
                    },
                ],
                // Flow 3 -- Fill in the required fields.
                [
                    {
                        content: "Fill in the name",
                        trigger: ".o_field_widget[name='name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR Curation Status Create",
                    },
                    {
                        content: "Fill in the code",
                        trigger: ".o_field_widget[name='code']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOURCST01",
                    },
                ],
                [
                    {
                        content: "Select the Category",
                        trigger: "select.o_field_widget[name='category']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text Eligible",
                    },
                ],
                [
                    // Flow 4 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Post-Condition -- a new record is created and active.
                    {
                        content: "Record is saved",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(TOUR Curation Status Create)",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only; do not trigger the default click action.
                        },
                    },
                ]
            )
        );
    }
);
