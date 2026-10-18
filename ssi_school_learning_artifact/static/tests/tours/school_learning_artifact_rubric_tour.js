// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact.school_learning_artifact_rubric_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Flow 1 of the IK: "Open the School > Configuration > Learning
        // Artifact > Rubrics menu." "Learning Artifact"
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
                    content: "Open the Rubrics menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_learning_artifact.school_learning_artifact_rubric_menu"]',
                },
                {
                    content: "Learning Artifact Rubrics list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Learning Artifact Rubrics)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // Selects an option from a many2one autocomplete dropdown.
        function pickMany2one(fieldName, label) {
            return [
                {
                    content: "Select the " + fieldName + " field value",
                    trigger: ".o_field_many2one[name='" + fieldName + "'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text " + label,
                },
                {
                    content: "Pick " + label + " from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                    in_modal: false,
                },
            ];
        }

        // IK: docs/school_learning_artifact_rubric/01-create.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_rubric_create",
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
                        run: "text TOUR Rubric Create",
                    },
                    {
                        content: "Fill in the code",
                        trigger: ".o_field_widget[name='code']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOURRBC01",
                    },
                ],
                pickMany2one("ethics_fail_status_id", "TOUR Fail Status"),
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
                            ".o_control_panel .breadcrumb-item.active:contains(TOUR Rubric Create)",
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
