# Create Graduate Profile

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_graduate_profile`\
> **Menu:** School > Configuration > Learning Artifact > Graduate Profiles\
> **Actor:** user in group `Graduate Profile`

## Pre-Condition

- **Access:** User is in group `Graduate Profile`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Graduate Profiles** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the graduate profile.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Sequence**: Defaults to **10**. When several profiles cover the same grade, the
     lowest sequence is used.
   - **Grades**: Optional. Select the grades covered by the profile.
4. Click **Save**.

## Post-Condition

- A new graduate profile is created and active.
- Learning artifacts of a class whose grade is listed take this profile in their
  **Graduate Profile** field.
