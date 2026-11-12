// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact_character.school_learning_artifact_character_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Selects an option from a many2one autocomplete dropdown.
        function pickMany2one(rootSelector, label) {
            return [
                {
                    content: "Type " + label,
                    trigger: rootSelector + " input",
                    run: "text " + label,
                },
                {
                    content: "Pick " + label + " from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(" + label + ")",
                },
            ];
        }

        // IK: docs/school_learning_artifact/11-tag-character.md
        tour.register(
            "ssi_school_learning_artifact_character_school_learning_artifact_" +
                "tag_character",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
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
                        content: "Learning Artifacts list is displayed",
                        trigger:
                            ".o_control_panel .breadcrumb-item.active:contains(Learning Artifacts)",
                        extra_trigger: ".o_list_view",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // Flow 2 -- Open the record to tag.
                    {
                        content: "Open the record",
                        trigger:
                            ".o_data_row:contains(TOUR CT Activity) .o_data_cell:first",
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
                    // Flow 4 -- Open the Character Tag tab.
                    {
                        content: "Open the Character Tag tab",
                        trigger: ".o_notebook .nav-link:contains(Character Tag)",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                ],
                // Flow 5 -- Select the Dominant Character Tags.
                pickMany2one(
                    ".o_field_many2manytags[name='dominant_subconstruct_ids']",
                    "TOUR CT Dominant"
                ),
                [
                    {
                        content: "The first dominant tag is added",
                        trigger:
                            ".o_field_many2manytags[name='dominant_subconstruct_ids'] .badge:contains(TOUR CT Dominant)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ],
                pickMany2one(
                    ".o_field_many2manytags[name='dominant_subconstruct_ids']",
                    "TOUR CT Another"
                ),
                // Flow 6 -- Select the Secondary Character Tags.
                pickMany2one(
                    ".o_field_many2manytags[name='secondary_subconstruct_ids']",
                    "TOUR CT Secondary"
                ),
                [
                    // Flow 7 -- Click Save.
                    {
                        content: "Save the record",
                        trigger: ".o_form_button_save",
                    },
                    {
                        // Post-Condition -- the tags are saved.
                        content: "The first dominant tag is saved",
                        trigger:
                            ".o_field_widget[name='dominant_subconstruct_ids']:contains(TOUR CT Dominant)",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "The second dominant tag is saved",
                        trigger:
                            ".o_field_widget[name='dominant_subconstruct_ids']:contains(TOUR CT Another)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "The secondary tag is saved",
                        trigger:
                            ".o_field_widget[name='secondary_subconstruct_ids']:contains(TOUR CT Secondary)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "The dominant tag codes are filled in",
                        trigger:
                            ".o_field_widget[name='dominant_subconstruct_codes']:contains(TOUR-CT-DOM)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
