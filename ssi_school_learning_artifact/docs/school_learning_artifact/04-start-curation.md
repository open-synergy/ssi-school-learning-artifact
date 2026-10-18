# Start Curation of Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** approver on the pending approval level\
> **State:** `confirm` → `open`\
> **Requires:** `02-submit`

## Pre-Condition

- **Record:** Status is **Waiting for Approval**.
- **Config:** An active `policy.template` grants `approve_ok` to the actor's group.
- **Access:** User is registered as an approver on the approval level that is currently
  **pending**. By default the approver is any user in group
  `School Learning Artifact — Validator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to curate.
3. Click the **Approve** button. This is the "Start Curation" action.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- If all approval levels are fulfilled, status changes automatically to **On Progress**,
  meaning the curation has started. The **Restart** button is no longer available, so
  the teacher cannot withdraw the artifact.
- If there are still pending approval levels, status remains **Waiting for Approval**
  and the next level becomes pending.
