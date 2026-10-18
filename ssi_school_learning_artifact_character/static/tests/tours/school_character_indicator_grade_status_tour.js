// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact_character.school_character_indicator_grade_status_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_character_indicator/01-set-grade-status.md
        tour.register(
            "ssi_school_learning_artifact_character_school_character_indicator_" +
                "set_grade_status",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 -- Open the Character Indicators menu.
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
                    content: "Open the Character Indicators menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_school_character.school_character_indicator_menu"]',
                },
                {
                    content: "Character Indicators list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Character Indicators)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Flow 2 -- Open the indicator to configure.
                {
                    content: "Open the indicator",
                    trigger:
                        ".o_data_row:contains(TOUR GS Indicator) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                // Flow 3 -- Click the Edit button.
                {
                    content: "Click Edit",
                    trigger: ".o_form_button_edit",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },
                // Flow 4 -- Open the Grade Status tab.
                {
                    content: "Open the Grade Status tab",
                    trigger: ".o_notebook .nav-link:contains(Grade Status)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                // Flow 5 -- Add a line.
                {
                    content: "Add a grade status line",
                    trigger:
                        ".o_field_widget[name='grade_status_ids'] " +
                        ".o_field_x2many_list_row_add a",
                },
                // Flow 6 -- Select the Grade Type.
                {
                    content: "Type the grade type",
                    trigger:
                        ".o_selected_row .o_field_many2one[name='grade_type_id'] input",
                    run: "text TOUR GS Grade Type",
                },
                {
                    content: "Pick the grade type from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR GS Grade Type)",
                },
                // Flow 7 -- Select the Status.
                {
                    content: "Select the status",
                    trigger: ".o_selected_row select.o_field_widget[name='status']",
                    run: "text Effective",
                },
                {
                    // Commit the line by clicking a field outside the list;
                    // do not commit with Tab on an editable list.
                    content: "Commit the grade status line",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },
                // Flow 8 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    // Post-Condition -- the line is listed.
                    content: "The grade status line is listed",
                    trigger:
                        ".o_field_widget[name='grade_status_ids'] " +
                        ".o_data_row:contains(TOUR GS Grade Type):contains(Effective)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        );
    }
);
