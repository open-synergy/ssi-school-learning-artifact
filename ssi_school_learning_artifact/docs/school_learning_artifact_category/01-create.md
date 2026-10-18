# Create Learning Artifact Category

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_category`\
> **Menu:** School > Configuration > Learning Artifact > Categories\
> **Actor:** user in group `Learning Artifact Category`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Category`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Categories** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the category.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Schools**: Optional. Select the schools that can use the category. Leave it empty
     to make the category available to every school.
4. Click **Save**.

## Post-Condition

- A new category is created and active.
- It becomes selectable in the **Category** field of the learning artifacts of the
  schools it applies to.
