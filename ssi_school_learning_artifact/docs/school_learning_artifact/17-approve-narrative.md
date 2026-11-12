# Approve Showcase Narrative

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** an approver of the **Standard** approval template of the showcase production\
> **Requires:** `15-request-narrative-approval`\
> **Inline Actions:** `action_reload_approval_template` (Restart Approval)

## Pre-Condition

- **Record:** The row of the channel in the **Production** table has **Status**
  **Waiting Approval**.
- **Config:** The **Standard** approval template of the showcase production has at least
  one approver detail. If it has none, **Approve** is refused with the message "No
  approver is configured": ask the administrator to add the approvers to the template,
  then a coordinator clicks **Restart Approval** of the row (a coordinator can click it
  while the row is **Waiting Approval**).
- **Access:** User is the approver whose turn it is, and can see the artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. In the **Production** table, find the row of the channel (**Status**: **Waiting
   Approval**).
5. Click the **Approve** button of the row.
6. Repeat with the next approver until the last approver has approved.
7. If the administrator changed the approvers while the row is **Waiting Approval**, a
   coordinator clicks the **Restart Approval** button of the row.

## Post-Condition

- After the last approver, the row **Status** is **Approved**; its **Content** stays
  locked and **Ready** can be checked.
- Each approval shows who approved and when (open the row to see them).
- An approver cannot approve before the approvers of the earlier sequence; an error
  message states it and the row stays **Waiting Approval**.
- **Restart Approval** removes the approvals and creates them again from the template,
  after the administrator changed the approvers.
