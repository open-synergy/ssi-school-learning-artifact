# Return Showcase Narrative to the Teacher

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `Learning Artifact Inventory Coordinator`\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** The artifact status is **Curated**, and its **Production** table has a row
  of the channel whose **Status** is **Draft**.
- **Access:** User is in group `Learning Artifact Inventory Coordinator` and can see the
  artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. In the **Production** table, find the row of the channel (**Status**: **Draft**).
5. Click the **Return to Teacher** button of the row.

## Post-Condition

- The row **Status** is **Assigned** and **Person in Charge** is the **Responsible**
  user (the teacher) of the artifact.
- The teacher receives a To-Do on the artifact that names the channel.
- While the row is **Assigned**, only the teacher and the coordinators can change its
  **Content**.
- If the user is not a coordinator, or the artifact is not **Curated**, an error message
  states it and the row stays **Draft**.
