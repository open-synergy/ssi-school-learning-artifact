// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_school_learning_artifact.school_learning_artifact_showcase_narrative_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        var PRODUCTION = ".o_field_widget[name='production_ids']";
        var ROW = PRODUCTION + " .o_data_row:contains(TOUR NR Channel)";

        // Flow 1 of every narrative IK: "Open the School > Learning Artifacts >
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

        // Clicks a button of the production row (read-only form) and waits for
        // the row to show the expected status. The status text cannot be in the
        // row before the action ran, so the wait is a real gate.
        function clickRowButton(buttonName, label, status) {
            return [
                {
                    content: "Click " + label + " on the row",
                    trigger: ROW + " button[name='" + buttonName + "']",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "The row status is " + status,
                    trigger: ROW + ":contains(" + status + ")",
                    run: function () {
                        // Assertion only.
                    },
                },
            ];
        }

        function openShowcase(activityName) {
            return [].concat(
                // Flow 1 -- Open the Learning Artifacts menu.
                openArtifactList(),
                // Flow 2 -- Open the curated record.
                openRecordByActivity(activityName),
                // Flow 3 -- Open the Showcase tab.
                openTab("Showcase")
            );
        }

        // IK: docs/school_learning_artifact/13-return-narrative-to-teacher.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_return_narrative_to_teacher",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Return Teacher"),
                // Flow 4 and 5 -- find the Draft row and click Return to Teacher.
                clickRowButton(
                    "action_assign_to_teacher",
                    "Return to Teacher",
                    "Assigned"
                )
            )
        );

        // IK: docs/school_learning_artifact/14-submit-narrative.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_submit_narrative",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Submit"),
                [
                    // Flow 4 -- Write the Content of the row (edit mode).
                    {
                        content: "Click Edit",
                        trigger: ".o_form_button_edit",
                        extra_trigger: ".o_form_view.o_form_readonly",
                    },
                    {
                        content: "Click the Content of the row",
                        trigger: ROW + " .o_data_cell[name='content']",
                        extra_trigger: ".o_form_view.o_form_editable",
                    },
                    {
                        content: "Write the narrative",
                        trigger: ".o_selected_row .o_field_widget[name='content']",
                        run: "text one two three four",
                    },
                    {
                        // Commit the line by clicking a field outside the list.
                        content: "Commit the production line",
                        trigger: ".o_field_widget[name='activity_name']",
                        run: function () {
                            this.$anchor[0].click();
                        },
                    },
                    // Flow 5 -- Click Save.
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
                // Flow 6 -- Click Submit on the row.
                clickRowButton("action_submit_narrative", "Submit", "Submitted")
            )
        );

        // IK: docs/school_learning_artifact/15-request-narrative-approval.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_request_narrative_approval",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Request"),
                // Flow 4 and 5 -- review the Submitted row and click Request Approval.
                clickRowButton(
                    "action_request_narrative_approval",
                    "Request Approval",
                    "Waiting Approval"
                )
            )
        );

        // IK: docs/school_learning_artifact/16-return-narrative.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_return_narrative",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Return"),
                // Flow 4 and 5 -- find the Submitted row and click Return.
                clickRowButton("action_return_narrative", "Return", "Assigned")
            )
        );

        // IK: docs/school_learning_artifact/17-approve-narrative.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_approve_narrative",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Approve"),
                // Flow 4 and 5 -- find the Waiting Approval row and click Approve. Flow 6 and 7 (next approver, Restart Approval) are skipped: the fixture has one approver and Restart Approval is conditional.
                clickRowButton("action_approve_approval", "Approve", "Approved")
            )
        );

        // IK: docs/school_learning_artifact/18-reject-narrative.md
        tour.register(
            "ssi_school_learning_artifact_school_learning_artifact_reject_narrative",
            {
                test: true,
                url: "/web",
            },
            [].concat(
                openShowcase("TOUR NR Reject"),
                // Flow 4 and 5 -- find the Waiting Approval row and click Reject.
                clickRowButton("action_reject_approval", "Reject", "Rejected")
            )
        );
    }
);
