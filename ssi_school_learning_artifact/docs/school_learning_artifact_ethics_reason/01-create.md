# Create Learning Artifact Ethics Reason

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_ethics_reason`\
> **Menu:** School > Configuration > Learning Artifact > Ethics Reasons\
> **Actor:** user in group `Learning Artifact Ethics Reason`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Ethics Reason`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Ethics Reasons** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the reason why an artifact can fail the ethics gate.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Schools**: Optional. Select the schools that can use the reason. Leave it empty
     to make the reason available to every school.
4. Click **Save**.

## Post-Condition

- A new ethics reason is created and active.
- It becomes selectable in the **Ethics Reason** field of the learning artifacts of the
  schools it applies to.
