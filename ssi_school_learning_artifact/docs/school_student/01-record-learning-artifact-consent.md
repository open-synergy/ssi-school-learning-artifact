# Record Learning Artifact Consent

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
  `docs/partner_consent_purpose/01-set-learning-artifact-usage.md`). Purposes without a
  usage are ignored by the learning artifacts.
- **Access:** User is in group `Learning Artifact Consent Officer`. The **Artifact
  Consents** button is hidden for everybody else.
- **Module:** `ssi_partner_data_privacy_consent` is installed.

## Flow

1. Open the **School > Students** menu.
2. Open the student to record the consent for.
3. Click the **Artifact Consents** smart button. The consents already recorded for the
   contact of the student are listed.
4. Click the **New** button. **(14.0: "Create")** The contact, the school of the student
   and the **Back Office** channel are already filled in.
5. Fill in the fields:
   - **Privacy Notice** _(required)_: Select the privacy notice version that the parent
     agreed to.
   - **Purpose** _(required)_: Select the purpose, for example the one that covers the
     publication of the artifact.
   - **Consent Type** _(required)_: **Granted** to give the consent, **Withdrawn** to
     take it back.
   - **Consent Level**: Shown when the type is **Granted**. Choose **Full** or
     **Limited**.
   - **Limited Preference**: Shown when the level is **Limited**. Write what the parent
     allows.
   - **Expiry Date**: Optional. Informative only; it does not change the consent shown
     on the artifacts.
6. Click **Save**.

## Post-Condition

- A new consent is added to the list of the student. It cannot be edited or deleted
  afterwards; to change a consent, record a new one.
- There is one consent per student per school: only the latest record for a purpose of
  the same school counts, so a student who moves to another unit needs a new consent in
  that unit.
- The **Parental Consent** tab of every learning artifact featuring the student shows
  the strictest consent of all its students: Refused, then Not Recorded, then Limited,
  then Full.
- If the inventory consent is **Withdrawn**, the artifact cannot be submitted.
