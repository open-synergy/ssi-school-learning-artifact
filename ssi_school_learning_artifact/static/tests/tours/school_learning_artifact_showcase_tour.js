// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact.school_learning_artifact_showcase_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Flow 1 of the showcase IK: "Open the School > Learning Artifacts >
        // Learning Artifacts menu."
        function openArtifactList() {
            return [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
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
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ];
        }

        // Opens the record identified by the unique Activity Name shown on the
        // list row (used as Pre-Condition test data marker).
        function openRecordByActivity(activityName) {
            return [
                {
                    content: "Open the record",
                    trigger:
                        ".o_data_row:contains(" + activityName + ") .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // Clicks Edit and waits for the edit mode.
        function clickEdit() {
            return [
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
            ];
        }

        // Opens a notebook page by its label.
        function openTab(label) {
            return [
                {
                    content: "Open the " + label + " tab",
                    trigger: ".o_notebook .nav-link:contains(" + label + ")",
                    extra_trigger: ".o_form_view",
                },
            ];
        }

        // Selects an option from a many2one autocomplete dropdown. The root
        // of a 14.0 many2one carries the field name; the dropdown is picked
        // by its unique label.
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

        // Clicks Save and waits for the read-only form.
        function clickSave() {
            return [
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/school_learning_artifact/08-select-for-showcase.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_select_for_showcase",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the curated record.
                openRecordByActivity("TOUR SH Select Activity"),
                // Flow 3 -- Click the Edit button.
                clickEdit(),
                // Flow 4 -- Open the Showcase tab.
                openTab("Showcase"),
                // Flow 5 -- Select the Showcase Stage.
                pickMany2one(
                    ".o_field_many2one[name='showcase_stage_id']",
                    "TOUR SH Selected"
                ),
                // Flow 6 -- Click Save.
                clickSave(),
                [
                    // Post-Condition -- the artifact is in the selected stage.
                    {
                        content: "The artifact is in the selected stage",
                        trigger:
                            ".o_field_widget[name='showcase_stage_id']:contains(TOUR SH Selected)",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_learning_artifact/09-produce-showcase.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_produce_showcase",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the curated record.
                openRecordByActivity("TOUR SH Produce Activity"),
                // Flow 3 -- Click the Edit button.
                clickEdit(),
                // Flow 4 -- Open the Showcase tab.
                openTab("Showcase"),
                // Flow 5 (optional) and 7 (optional) are skipped.
                [
                    // Flow 6 -- Add a line to the Production table.
                    {
                        content: "Add a production line",
                        trigger:
                            ".o_field_widget[name='production_ids'] " +
                            ".o_field_x2many_list_row_add a",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                ],
                pickMany2one(
                    ".o_selected_row .o_field_many2one[name='channel_id']",
                    "TOUR SH Channel"
                ),
                [
                    {
                        content: "Fill in the Content",
                        trigger: ".o_selected_row .o_field_widget[name='content']",
                        run: "text one two three four",
                    },
                    {
                        // Commit the line by clicking a field outside the list;
                        // do not commit with Tab on an editable list.
                        content: "Commit the production line",
                        trigger: ".o_field_widget[name='activity_name']",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                ],
                // Flow 8 -- Click Save.
                clickSave(),
                [
                    // Post-Condition -- the row is listed with its word count.
                    {
                        content: "The production row is listed",
                        trigger:
                            ".o_field_widget[name='production_ids'] .o_data_row:contains(TOUR SH Channel):contains(one two three four)",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );

        // IK: docs/school_learning_artifact/10-review-limited-consent.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_review_limited_consent",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the curated record.
                openRecordByActivity("TOUR SH Review Activity"),
                // Flow 3 -- Check the consent preference of the students.
                openTab("Parental Consent"),
                [
                    {
                        content: "The publication consent is limited",
                        trigger:
                            ".o_field_widget[name='publication_consent']:contains(Limited)",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    // Flow 4 -- Click the Mark Consent Reviewed button.
                    {
                        content: "Click Mark Consent Reviewed",
                        trigger:
                            ".o_statusbar_buttons button[name='action_mark_consent_reviewed']",
                        extra_trigger: ".o_form_view.o_form_readonly",
                    },
                ],
                // Post-Condition -- the consent is marked as reviewed.
                openTab("Showcase"),
                [
                    {
                        content: "Consent Reviewed is checked",
                        trigger:
                            ".o_field_widget[name='consent_reviewed'] input:checked, " +
                            ".o_field_widget[name='consent_reviewed']:checked",
                        extra_trigger: ".o_form_view.o_form_readonly",
                        run: function () {
                            // Assertion only.
                        },
                    },
                    {
                        content: "Showcase Consent OK is checked",
                        trigger:
                            ".o_field_widget[name='showcase_consent_ok'] input:checked, " +
                            ".o_field_widget[name='showcase_consent_ok']:checked",
                        run: function () {
                            // Assertion only.
                        },
                    },
                ]
            )
        );
    }
);
