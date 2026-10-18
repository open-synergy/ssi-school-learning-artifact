# Reopen Learning Artifact for Revision

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — Validator`\
> **State:** `done` → `draft`\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** Status is **Curated** and the **Curation Status Category** is **Needs
  Revision**.
- **Record:** **Revision Count** is lower than the **Maximum Revision** of the rubric.
- **Config:** An active `policy.template` for this model grants `restart_ok` for state
  `done`, limited to the artifacts above, to the actor's group.
- **Access:** User is in group `School Learning Artifact — Validator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to reopen.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**, so the artifact can be improved and submitted again.
- **Revision Count** increases by one. The scores and the curation notes are kept.
- If the category is not **Needs Revision** or the revision limit is reached, the
  **Restart** button is not available.
