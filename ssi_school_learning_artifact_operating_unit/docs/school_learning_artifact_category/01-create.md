# Create Learning Artifact Category (Operating Unit)

> **Module:** `ssi_school_learning_artifact_operating_unit`\
> **Extends:** ssi_school_learning_artifact — model `school_learning_artifact_category`,
> action `01-create`

## Additional Pre-Condition

- **Access:** The **Operating Unit** field is shown only to users in the group _Multiple
  Operating Unit_.

## Modified Flow

Anchor: after step 3 of the base work instruction (the fields are filled in, before
Save):

1. Check the **Operating Unit** field.
2. Select the operating units that can use the category. Leave it empty to make the
   category available to every operating unit.

## Additional Post-Condition

- The saved record shows the **Operating Unit** in the form.
- It becomes selectable in the **Category** field of the learning artifacts of the
  selected operating units only.

## Modified — Record Visibility

- Every user only sees the category records without operating unit or with one of the
  operating units of the user, whatever the group of the user. The rule limits reading
  only.
