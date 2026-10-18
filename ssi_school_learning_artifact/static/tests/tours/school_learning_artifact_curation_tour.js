// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact.school_learning_artifact_curation_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // Flow 1 of the curate and reopen IK: "Open the School > Learning
        // Artifacts > Learning Artifacts menu."
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

        // Clicks a header button, answers the confirmation dialog and waits for
        // the target status in the statusbar.
        function clickAndConfirm(buttonName, label, status, statusLabel) {
            return [
                {
                    content: "Click the " + label + " button",
                    trigger: ".o_statusbar_buttons button[name='" + buttonName + "']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is " + statusLabel,
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='" +
                        status +
                        "'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        // IK: docs/school_learning_artifact/06-curate.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_curate",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the record to curate.
                openRecordByActivity("TOUR LC Curate Activity"),
                [
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

                    // Flow 4 -- Open the Curation tab.
                    {
                        content: "Open the Curation tab",
                        trigger: ".o_notebook .nav-link:contains(Curation)",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },

                    // Flow 5 -- Select the Ethics Result.
                    {
                        content: "Select the Ethics Result",
                        trigger: "select.o_field_widget[name='ethics_result']",
                        extra_trigger: ".o_form_view.o_form_editable",
                        run: "text Pass",
                    },

                    // Flow 6 -- Enter the score of the aspect row.
                    {
                        content: "Click the Score cell of the aspect row",
                        trigger:
                            ".o_data_row:contains(TOUR Aspect One) .o_data_cell[name='score']",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        content: "Enter the score",
                        trigger: ".o_selected_row .o_field_widget[name='score']",
                        run: "text 3",
                    },

                    // Flow 7 -- Click Save.
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
                ],
                // Flow 9 and 10 -- Click Done, then OK on the dialog.
                clickAndConfirm("action_done", "Done", "done", "Curated")
            )
        );

        // IK: docs/school_learning_artifact/07-reopen.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_reopen",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the record to reopen.
                openRecordByActivity("TOUR LC Reopen Activity"),
                // Flow 3 and 4 -- Click Restart, then OK on the dialog.
                clickAndConfirm("action_restart", "Restart", "draft", "Draft")
            )
        );
    }
);
