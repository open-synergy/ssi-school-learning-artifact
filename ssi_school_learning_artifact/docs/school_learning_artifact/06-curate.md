# Curate Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — Validator`\
> **State:** `open` → `done`\
> **Requires:** `04-start-curation`

## Pre-Condition

- **Record:** Status is **On Progress** and a rubric applies to the school of the
  artifact. The artifact has one row in the **Scores** table per aspect of the rubric,
  ethics gate aspects included.
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Config:** The rubric defines the thresholds and the curation statuses, and has at
  least one aspect of type **Ethics Gate**. Every aspect lists its levels (see
  `school_learning_artifact_rubric/01-create`).
- **Access:** User is in group `School Learning Artifact — Validator`. When an aspect
  lists assessor groups, the user is in those groups too.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to curate.
3. Click the **Edit** button.
4. Open the **Curation** tab.
5. In the **Scores** table, click the **Level** cell of each ethics gate row and select
   the level that answers the question. The **Ethics Result** is **Fail** as soon as one
   answer fails the gate, and **Pass** when every gate row is answered without a failing
   level.
6. Click the **Level** cell of each scored aspect row and select the level whose text
   describes the artifact. The **Level Text** column shows the whole text of the picked
   level. Skip this step when the Ethics Result is **Fail**: the scored aspect rows are
   locked.
7. Click **Save**. The **Score** of each row, the **Total Score** and the **Curation
   Status** are calculated.
8. When the status needs a revision, fill in the **Recommendation**. When the status is
   **Not Eligible**, fill in the **Curator Note** with the reason of the archive. Click
   **Save**.
9. Click the **Done** button.
10. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Curated**. The curator and the time are recorded in **Curated By**
  and **Curated On**.
- If the rubric has no ethics gate aspect, an ethics gate row is not answered, a scored
  aspect has no level (Ethics Result **Pass**), the recommendation or the curator note
  required by the status is empty, or the assessor rules of the rubric are broken, the
  artifact stays **On Progress** and an error message states the missing item.
