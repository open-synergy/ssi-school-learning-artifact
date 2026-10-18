// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_learning_artifact.school_student_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of the IK: "Open the School > Students menu."
    function openStudentList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the School app",
                trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
            },
            {
                content: "Open the Students menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_school.school_student_menu"]',
            },
            {
                // Gate: wait for the TARGET action, not just any list.
                content: "Students list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Students)",
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

    // IK: docs/school_student/01-record-learning-artifact-consent.md
    tour.register(
        "ssi_school_learning_artifact_school_student_record_learning_artifact_consent",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Students menu.
            openStudentList(),
            [
                // Flow 2 -- Open the student record.
                {
                    content: "Open the student",
                    trigger: ".o_data_row:contains(TOUR LC Student) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                // Flow 3 -- Click the Artifact Consents smart button.
                {
                    content: "Click the Artifact Consents smart button",
                    trigger:
                        ".oe_button_box button[name='action_open_learning_artifact_consent']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Consent list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Data Privacy Consents)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                // Flow 4 -- Click the New button. (14.0: "Create")
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
            // Flow 5 -- Fill in the consent.
            pickMany2one("notice_id", "TOUR LC Notice"),
            pickMany2one("purpose_id", "TOUR LC Publication Purpose"),
            [
                {
                    content: "Select the Consent Level",
                    trigger: "select.o_field_widget[name='consent_level']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Limited",
                },
                {
                    content: "Fill in the Limited Preference",
                    trigger: ".o_field_widget[name='limited_preference']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Only inside the school",
                },

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // Post-Condition -- the consent is saved and listed.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Back to the consent list",
                    trigger:
                        ".o_control_panel .breadcrumb-item:not(.active):contains(Data Privacy Consents)",
                },
                {
                    content: "The consent is listed",
                    trigger:
                        ".o_list_view .o_data_row:contains(TOUR LC Publication Purpose)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        )
    );
});
