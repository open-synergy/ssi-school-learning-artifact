# Withdraw Learning Artifact from Curation

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **State:** `confirm` → `draft`\
> **Requires:** `02-submit`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**. Once the curator has started the
  curation (status **On Progress**), the artifact can no longer be withdrawn.
- **Config:** An active `policy.template` for this model grants `restart_ok` for state
  `confirm` to the actor's group.
- **Access:** User is in group `School Learning Artifact — User`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to withdraw.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**, so the artifact can be edited again.
- All approval records are removed and the approval template is cleared. A later Submit
  starts the approval process from the beginning.
