# Set the Final Status of a Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — Validator`\
> **State:** `open` → `done`\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** Status is **On Progress**, the curation was already started again after a
  revision, and the **Revision Count** is equal to or higher than the **Maximum
  Revision** of the rubric.
- **Record:** The ethics gate is answered and every scored aspect has a level, so that
  the scores still give a status of the category **Needs Revision**. The
  **Recommendation** is filled in.
- **Data:** At least one curation status of the category **Archive** or **Not Eligible**
  is active and is open to the school of the artifact (or to every school).
- **Config:** An active `policy.template` for this model grants `done_ok` for state
  `open` to the actor's group.
- **Access:** User is in group `School Learning Artifact — Validator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to curate.
3. Click the **Edit** button.
4. Open the **Curation** tab.
5. In the **Final Curation Status** field, select the status that closes the artifact:
   **Archive** keeps it as an internal archive, **Not Eligible** marks it as not
   suitable. The field is shown only when the revision limit is reached.
6. When the status is **Not Eligible**, fill in the **Curator Note** with the reason.
7. Click **Save**.
8. Click the **Done** button.
9. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Curated**. The **Curation Status** is the status that was picked
  in **Final Curation Status**, so the **Curation Status Category** is **Archive** or
  **Not Eligible**.
- The **Restart** button is not available any more.
- If the **Final Curation Status** is empty while the revision limit is reached, or it
  is filled while the revision limit is not reached, the artifact stays **On Progress**
  and an error message states what to correct. A **Not Eligible** status without a
  **Curator Note** is rejected the same way.
