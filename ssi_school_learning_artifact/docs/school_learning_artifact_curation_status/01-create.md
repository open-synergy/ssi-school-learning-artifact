# Create Learning Artifact Curation Status

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_curation_status`\
> **Menu:** School > Configuration > Learning Artifact > Curation Statuses\
> **Actor:** user in group `Learning Artifact Curation Status`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Curation Status`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Curation Statuses** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the label that the school shows to its users.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Category** _(required)_: Select **Eligible**, **Needs Revision**, **Archive** or
     **Not Eligible**. Other modules read only the category, never the name.
   - **Schools**: Optional. Select the schools that can use the status. Leave it empty
     to make the status available to every school.
4. Click **Save**.

## Post-Condition

- A new curation status is created and active.
- It becomes selectable in the **Ethics Fail Status**, **Knockout Status** and threshold
  **Status** fields of the rubrics.
