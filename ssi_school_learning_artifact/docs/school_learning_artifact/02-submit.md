# Submit Learning Artifact for Curation

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **State:** `draft` → `confirm`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Record:** At least one **Student** is selected.
- **Record:** **Learning Area**, **Category**, **Description** and **Link** are filled
  in.
- **Record:** If the school defines a link prefix, the **Link** starts with it.
- **Record:** If the school requires a component, a dimension or a phase, the **Primary
  Component**, **Dimension** or **Phase** is filled in.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group.
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level.
- **Access:** User is in group `School Learning Artifact — User`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to submit.
3. Click the **Confirm** button. This is the "Submit for Curation" action.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the approval template.
- If a precondition above is not met, the artifact stays in **Draft** and an error
  message states the missing item.
