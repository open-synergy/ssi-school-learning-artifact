# Submit Showcase Narrative

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** the teacher assigned in **Person in Charge**, or a user in group `Learning Artifact Inventory Coordinator`\
> **Requires:** `13-return-narrative-to-teacher`

## Pre-Condition

- **Record:** The row of the channel in the **Production** table has **Status**
  **Assigned**.
- **Config:** The channel may limit the narrative with **Minimum Words** and **Maximum
  Words** (see `school_learning_artifact_showcase_channel/01-create`). A limit of 0
  means no limit. For example: newsletter 150 to 250 words, physical caption 30 to 50,
  portal 80 to 100, Instagram 80 to 120, Facebook 150 to 250.
- **Access:** User is the **Person in Charge** of the row, or is in group
  `Learning Artifact Inventory Coordinator`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. Click the **Edit** button.
5. In the **Production** table, click the **Content** of the row and write the
   narrative. The **Word Count** shows the number of words.
6. Click **Save**.
7. Click the **Submit** button of the row.

## Post-Condition

- The row **Status** is **Submitted** and its **Content** is locked.
- If the **Word Count** is below **Minimum Words** or above **Maximum Words** of the
  channel, an error message states the count and the limit, and the row stays
  **Assigned**.
- If the user is neither the **Person in Charge** nor a coordinator, an error message
  states it and the row stays **Assigned**.
