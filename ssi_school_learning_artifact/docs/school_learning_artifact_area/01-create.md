# Create Learning Artifact Area

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_area`\
> **Menu:** School > Configuration > Learning Artifact > Areas\
> **Actor:** user in group `Learning Artifact Area`

## Pre-Condition

- **Data:** The school unit that owns the learning area exists.
- **Access:** User is in group `Learning Artifact Area`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Areas** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the learning area (e.g. "Mathematics",
     "Robotics Club").
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **School** _(required)_: Select the school unit that owns this learning area.
   - **Area Type** _(required)_: Select **Subject**, **Activity Area**, **Development
     Area** or **Competition Field**.
4. Click **Save**.

## Post-Condition

- A new learning area is created and active.
- It becomes selectable in the **Learning Area** field of the learning artifacts of the
  same school.
