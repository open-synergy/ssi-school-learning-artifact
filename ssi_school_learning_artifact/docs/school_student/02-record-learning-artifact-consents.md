# Record Learning Artifact Consents

> **Module:** `ssi_school_learning_artifact`\
> **Extends:** ssi_school — model `school_student`\
> **Model:** `school_student`\
> **Menu:** School > Students\
> **Actor:** user in group `Learning Artifact Consent Officer`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The student already exists and is linked to a contact.
- **Record:** A privacy notice exists (Contacts > Configuration > Data Privacy > Privacy
  Notice).
- **Config:** At least one consent purpose has a **Learning Artifact Usage** (see
  `docs/partner_consent_purpose/01-set-learning-artifact-usage.md`). A usage that is
  covered by exactly one purpose gets that purpose automatically; when several purposes
  cover the usage, the purpose is chosen on the row.
- **Access:** User is in group `Learning Artifact Consent Officer`. The **Record
  Consents** button is hidden for everybody else.
- **Module:** `ssi_partner_data_privacy_consent` is installed.

## Flow

1. Open the **School > Students** menu.
2. Open the student to record the consents for.
3. Click the **Record Consents** smart button. A dialog opens with the student, the
   school of the student and four rows: **Inventory**, **Internal Assessment**,
   **Publication** and **Promotion**.
4. Fill in the fields that are shared by all rows:
   - **Privacy Notice** _(required)_: Select the privacy notice version that the parent
     agreed to.
   - **Consent Date** _(required)_: Defaults to now.
   - **Channel** _(required)_: Defaults to **Back Office**.
   - **Expiry Date**: Optional. Informative only; it does not change the consent shown
     on the artifacts.
5. On each usage row that the parent decided about, fill in the fields. A row without a
   **Consent Type** is skipped:
   - **Purpose**: Filled in when only one purpose covers the usage; otherwise select it.
   - **Consent Type**: **Granted** to give the consent, **Withdrawn** to take it back.
   - **Consent Level** _(required when granted)_: Choose **Full** or **Limited**.
   - **Limited Preference**: Available when the level is **Limited**. Write what the
     parent allows.
6. Click **Save**.

## Post-Condition

- The dialog closes. One consent is added to the log of the contact of the student for
  every row that had a **Consent Type**; rows without one create nothing. All the
  consents share the notice, the school, the date, the channel and the expiry date.
- If a row is not valid — no row has a consent type, a row has no purpose, or a granted
  row has no consent level — an error is shown and no consent is created at all.
- Consents cannot be edited or deleted afterwards; to change a consent, record a new
  one.
- The **Parental Consent** tab of every learning artifact featuring the student, the
  ethics gate and the showcase follow the new consents as described in
  `01-record-learning-artifact-consent.md`.
