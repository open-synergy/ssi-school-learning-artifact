# Create Graduate Profile (Operating Unit)

> **Module:** `ssi_school_learning_artifact_operating_unit`\
> **Extends:** ssi_school_learning_artifact — model `school_graduate_profile`, action `01-create`

## Additional Pre-Condition

- **Access:** The **Operating Unit** field is shown only to users in the group _Multiple
  Operating Unit_.

## Modified Flow

Anchor: after step 3 of the base work instruction (the fields are filled in, before
Save):

1. Check the **Operating Unit** field.
2. Select the operating units that can use the graduate profile. Leave it empty to make
   the profile available to every operating unit.

## Additional Post-Condition

- The saved record shows the **Operating Unit** in the form.
- A learning artifact takes the profile that lists its operating unit before the
  profiles without operating unit, whatever their **Sequence**. When no profile lists
  its operating unit, the profile without operating unit that has the lowest
  **Sequence** is taken. A profile of another operating unit is never taken.

## Modified — Record Visibility

- Every user only sees the graduate profiles without operating unit or with one of the
  operating units of the user, whatever the group of the user. The rule limits reading
  only.
