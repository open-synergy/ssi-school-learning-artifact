# Curate Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — Validator`\
> **State:** `open` → `done`\
> **Requires:** `04-start-curation`

## Pre-Condition

- **Record:** Status is **On Progress** and a rubric applies to the school of the
  artifact. The artifact has one score row per aspect of the rubric.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Config:** The rubric defines the aspects, the thresholds and the curation statuses
  (see `school_learning_artifact_rubric/01-create`).
- **Access:** User is in group `School Learning Artifact — Validator`. When the aspects
  or the ethics gate list assessor groups, the user is in those groups too.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to curate.
3. Click the **Edit** button.
4. Open the **Curation** tab.
5. Select the **Ethics Result**. When it is **Fail**, select the **Ethics Reason**.
6. Click the **Score** cell of each row in the **Scores** table and enter the score of
   the aspect. Skip this step when the Ethics Result is **Fail**.
7. Click **Save**. The **Total Score** and the **Curation Status** are calculated.
8. When the status needs a revision, fill in the **Recommendation**. When the status is
   **Not Eligible**, fill in the **Curator Note** with the reason of the archive. Click
   **Save**.
9. Click the **Done** button.
10. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Curated**. The curator and the time are recorded in **Curated By**
  and **Curated On**.
- If the Ethics Result is empty, an aspect is not scored (Ethics Result **Pass**), the
  recommendation or the curator note required by the status is empty, or the assessor
  rules of the rubric are broken, the artifact stays **On Progress** and an error
  message states the missing item.
