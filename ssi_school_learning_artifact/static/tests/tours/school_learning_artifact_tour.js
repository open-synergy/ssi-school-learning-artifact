// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_learning_artifact.school_learning_artifact_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every school_learning_artifact IK: "Open the School >
    // Learning Artifacts > Learning Artifacts menu."
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

    // IK: docs/school_learning_artifact/01-create.md
    tour.register(
        "ssi_school_learning_artifact_school_learning_artifact_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Learning Artifacts menu.
            openArtifactList(),
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
                        // Assertion only.
                    },
                },
            ],
            // Flow 3 -- Fill in the required fields. The school comes first
            // because changing it clears the dependent fields.
            pickMany2one("school_id", "TOUR LA School"),
            pickMany2one("academic_year_id", "TOUR LA Year"),
            pickMany2one("grade_class_id", "TOUR LA Class"),
            [
                {
                    content: "Fill in the Activity Name",
                    trigger: ".o_field_widget[name='activity_name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR LA Created Activity",
                },
                {
                    content: "Select the Media Type",
                    trigger: "select.o_field_widget[name='media_type']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Photo",
                },

                // Flow 4 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- a new record is created in Draft status.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/school_learning_artifact/02-submit.md
    tour.register(
        "ssi_school_learning_artifact_school_learning_artifact_submit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Learning Artifacts menu.
            openArtifactList(),
            // Flow 2 -- Open the record to submit.
            openRecordByActivity("TOUR LA Submit Activity"),
            // Flow 3 and 4 -- Click Confirm, then OK on the dialog.
            clickAndConfirm(
                "action_confirm",
                "Confirm",
                "confirm",
                "Waiting for Approval"
            )
        )
    );

    // IK: docs/school_learning_artifact/03-withdraw.md
    tour.register(
        "ssi_school_learning_artifact_school_learning_artifact_withdraw",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Learning Artifacts menu.
            openArtifactList(),
            // Flow 2 -- Open the record to withdraw.
            openRecordByActivity("TOUR LA Withdraw Activity"),
            // Flow 3 and 4 -- Click Restart, then OK on the dialog.
            clickAndConfirm("action_restart", "Restart", "draft", "Draft")
        )
    );

    // IK: docs/school_learning_artifact/04-start-curation.md
    tour.register(
        "ssi_school_learning_artifact_school_learning_artifact_start_curation",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Learning Artifacts menu.
            openArtifactList(),
            // Flow 2 -- Open the record to curate.
            openRecordByActivity("TOUR LA Curation Activity"),
            // Flow 3 and 4 -- Click Approve, then OK on the dialog.
            clickAndConfirm("action_approve_approval", "Approve", "open", "On Progress")
        )
    );

    // IK: docs/school_learning_artifact/05-cancel.md
    tour.register(
        "ssi_school_learning_artifact_school_learning_artifact_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Learning Artifacts menu.
            openArtifactList(),
            // Flow 2 -- Open the record to cancel.
            openRecordByActivity("TOUR LA Cancel Activity"),
            [
                // Flow 3 -- Click the Cancel button.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- In the wizard, select the Cancellation Reason
                // (radio widget).
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] " +
                        ".o_radio_item:contains(TOUR LA Cancel Reason) input",
                    run: "click",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the Are you sure? dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
