# Review Limited Publication Consent of Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in the consent reviewer group of the school\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** Status is **Curated**, **Consent Review Required** is checked and
  **Consent Reviewed** is not checked yet.
- **Config:** On the **Learning Artifact** tab of the school, **Showcase Limited Consent
  Treatment** is **Review Task**. When **Showcase Consent Reviewer Group** is filled in,
  only its users can do this task.
- **Access:** User is in the consent reviewer group of the school, and can see the
  artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Check the preference of the students who limited the publication in the **Parental
   Consent** tab.
4. Click the **Mark Consent Reviewed** button.

## Post-Condition

- **Consent Reviewed** is checked and **Consent Reviewed By** shows the user. The **Mark
  Consent Reviewed** button is no longer available.
- **Showcase Consent OK** is checked, so the artifact can move into a stage that
  requires the publication consent.
- If the user is outside the consent reviewer group, an error message states it and the
  artifact stays unreviewed.
