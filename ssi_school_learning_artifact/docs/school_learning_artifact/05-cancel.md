# Cancel Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **State:** `draft` | `confirm` | `reject` → `cancel`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval**, or **Rejected**. Once the
  curation has started (**On Progress**), the artifact can no longer be cancelled.
- **Config:** An active `base.cancel_reason` exists that is usable for this model.
- **Config:** An active `policy.template` grants `cancel_ok` for that state to the
  actor's group.
- **Access:** User is in group `School Learning Artifact — User`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Cancellation Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The artifact is archived by status, not deleted: it stays visible in the list.
