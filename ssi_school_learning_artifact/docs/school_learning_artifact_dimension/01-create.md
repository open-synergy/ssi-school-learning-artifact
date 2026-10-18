# Create Learning Artifact Dimension

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_dimension`\
> **Menu:** School > Configuration > Learning Artifact > Dimensions\
> **Actor:** user in group `Learning Artifact Dimension`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Dimension`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Dimensions** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the dimension.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Schools**: Optional. Select the schools that can use the dimension. Leave it
     empty to make the dimension available to every school.
4. Click **Save**.

## Post-Condition

- A new dimension is created and active.
- It becomes selectable in the **Dimension** field of the learning artifacts of the
  schools it applies to.
