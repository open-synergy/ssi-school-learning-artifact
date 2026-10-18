# Create Learning Artifact (Operating Unit)

> **Module:** `ssi_school_learning_artifact_operating_unit`\
> **Extends:** ssi_school_learning_artifact — model `school_learning_artifact`, action `01-create`

## Additional Pre-Condition

- **Config:** The school of the artifact is linked to its operating unit. A school with
  exactly one operating unit fills the **Operating Unit** of the artifact automatically.
- **Access:** The **Operating Unit** field is shown only to users in the group _Multiple
  Operating Unit_.

## Modified Flow

Anchor: after step 3 of the base work instruction (the **School** is selected, before
Save):

1. Check the **Operating Unit** field. It is filled from the school when the school
   belongs to exactly one operating unit. Otherwise it keeps the default operating unit
   of the current user.
2. Change the **Operating Unit** manually if needed. A value entered manually is kept on
   save.

## Additional Post-Condition

- The saved artifact shows the **Operating Unit** in the form.
- Changing the **School** of an existing artifact to a school with exactly one operating
  unit sets the **Operating Unit** to that unit again.

## Modified — Record Visibility

- Users in the _Operating Unit_ group only see, edit and delete the artifacts whose
  Operating Unit is one of their own Operating Units. The users in the _Company_ group
  of the learning artifact are not restricted by this rule.
