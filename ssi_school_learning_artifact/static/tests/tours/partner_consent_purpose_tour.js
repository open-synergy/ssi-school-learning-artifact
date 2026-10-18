// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_school_learning_artifact.partner_consent_purpose_tour", function (
    require
) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/partner_consent_purpose/01-set-learning-artifact-usage.md
    tour.register(
        "ssi_school_learning_artifact_partner_consent_purpose_set_learning_artifact_usage",
        {
            test: true,
            url: "/web",
        },
        [
            // Flow 1 -- Open the Contacts > Configuration > Data Privacy >
            // Consent Purpose menu. "Data Privacy" is a grouping menuitem
            // without action, rendered by 14.0 as a non-clickable dropdown
            // header, so there is no step for it.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Contacts app",
                trigger: '.o_app[data-menu-xmlid="contacts.menu_contacts"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_partner.res_partner_menu_config"]',
            },
            {
                content: "Open the Consent Purpose menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_partner_data_privacy_consent.partner_consent_purpose_menu"]',
            },
            {
                content: "Consent Purpose list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Consent Purpose)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            // Flow 2 -- Open the purpose.
            {
                content: "Open the purpose",
                trigger:
                    ".o_data_row:contains(TOUR LC Usage Purpose) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            // Flow 3 -- Click the Edit button. (14.0 only)
            {
                content: "Click Edit",
                trigger: ".o_form_button_edit",
                extra_trigger: ".o_form_view.o_form_readonly",
            },
            // Flow 4 -- Select the Learning Artifact Usage.
            {
                content: "Select the Learning Artifact Usage",
                trigger: "select.o_field_widget[name='learning_artifact_usage']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text Publication",
            },
            // Flow 5 -- Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition -- the usage is saved on the purpose.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "The usage is shown",
                trigger:
                    ".o_form_view.o_form_readonly .o_field_widget[name='learning_artifact_usage']:contains(Publication)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
