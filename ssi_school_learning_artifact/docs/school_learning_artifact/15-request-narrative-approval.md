# Request Approval of Showcase Narrative

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `Learning Artifact Inventory Coordinator`\
> **Requires:** `14-submit-narrative`

## Pre-Condition

- **Record:** The row of the channel in the **Production** table has **Status**
  **Submitted**.
- **Config:** The administrator added the approvers, in sequence, as details of the
  **Standard** approval template of the showcase production (for example the principal
  first, then the branch person in charge). A template without detail keeps the
  narrative waiting: nobody can approve it.
- **Access:** User is in group `Learning Artifact Inventory Coordinator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. In the **Production** table, find the row of the channel (**Status**: **Submitted**)
   and review its **Content**.
5. Click the **Request Approval** button of the row.

## Post-Condition

- The row **Status** is **Waiting Approval**.
- When you open the row, the approvals of the template are listed in sequence, and only
  the first approver can approve.
- If the user is not a coordinator, an error message states it and the row stays
  **Submitted**.
