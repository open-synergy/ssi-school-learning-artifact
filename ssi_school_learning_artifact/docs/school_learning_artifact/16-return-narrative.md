# Return Showcase Narrative for Revision

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `Learning Artifact Inventory Coordinator`\
> **Requires:** `14-submit-narrative`

## Pre-Condition

- **Record:** The row of the channel in the **Production** table has **Status**
  **Submitted** or **Rejected**.
- **Config:** On the **Learning Artifact** tab of the school, **Showcase Narrative
  Revision Limit** (1 by default) is how many times the narrative can go back to the
  teacher.
- **Access:** User is in group `Learning Artifact Inventory Coordinator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. In the **Production** table, find the row of the channel (**Status**: **Submitted**
   or **Rejected**).
5. Click the **Return** button of the row.

## Post-Condition

- The row **Status** is **Assigned**. The approvals of a rejected narrative are removed.
- While **Revision Count** is below the limit of the school, **Person in Charge** is the
  teacher, **Revision Count** grows by one and the teacher receives a new To-Do.
- Beyond the limit, **Person in Charge** is the user who clicked **Return**, **Revision
  Count** stays and no To-Do is created: the coordinator revises the narrative and
  submits it again.
- If the user is not a coordinator, an error message states it and the row keeps its
  status.
