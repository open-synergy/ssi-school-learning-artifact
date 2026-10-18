// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact_operating_unit.school_learning_artifact_operating_unit_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

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

        // IK: docs/school_learning_artifact/01-create.md
        tour.register(
            "ssi_school_learning_artifact_operating_unit_school_learning_artifact_create",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Base Flow 1 -- Open the Learning Artifacts menu.
                [
                    tour.stepUtils.showAppsMenuItem(),
                    {
                        content: "Open the School app",
                        trigger:
                            '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                    },
                    {
                        content: "Open the Learning Artifacts section",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_school_learning_artifact.menu_school_learning_artifact"]',
                    },
                    {
                        content: "Open the Learning Artifacts menu",
                        trigger:
                            '.o_menu_sections [data-menu-xmlid="ssi_school_learning_artifact.school_learning_artifact_menu"]',
                    },
                    {
                        // Gate: wait for the TARGET action, not just any list.
                        content: "Learning Artifacts list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(Learning Artifacts)",
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
                ],
                // Base Flow 3 -- Fill in the required fields. The school
                // comes first because it derives the operating unit.
                pickMany2one("school_id", "TOUR OU School"),
                [
                    // Delta Flow 1 -- The Operating Unit field is shown.
                    {
                        content: "Operating Unit field is displayed",
                        trigger: ".o_field_widget[name='operating_unit_id'] input",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                pickMany2one("academic_year_id", "TOUR OU Year"),
                pickMany2one("grade_class_id", "TOUR OU Class"),
                [
                    {
                        content: "Fill in the Activity Name",
                        trigger: ".o_field_widget[name='activity_name']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text TOUR OU Created Activity",
                    },
                    {
                        content: "Select the Media Type",
                        trigger: "select.o_field_widget[name='media_type']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text Photo",
                    },

                    // Base Flow 4 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },

                    // Delta Post-Condition -- the saved form shows the
                    // Operating Unit derived from the school.
                    {
                        content: "Record is saved",
                        trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Operating Unit of the school is displayed",
                        trigger:
                            ".o_field_widget[name='operating_unit_id']:contains(TOUR OU Unit)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
