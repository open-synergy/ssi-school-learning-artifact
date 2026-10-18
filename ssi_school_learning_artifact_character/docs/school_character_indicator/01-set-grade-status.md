# Set Grade Status of Character Indicator

> **Module:** `ssi_school_learning_artifact_character`\
> **Model:** `school_character_indicator`\
> **Extends:** ssi_school_character — model `school_character_indicator`\
> **Menu:** School > Configuration > Character Indicators\
> **Actor:** user in group `Character Learning — User`\
> **Requires:** `ssi_school_character/school_character_indicator/01-create`

## Pre-Condition

- **Record:** A **Character Indicator** exists and is active. Its **Sub-construct** is
  filled in, otherwise the indicator does not open any character tag.
- **Data:** At least one **Grade Type** exists
  (`ssi_school/school_grade_type/01-create`).
- **Access:** User is in group `Character Learning — User`.

## Flow

1. Open the **School > Configuration > Character Indicators** menu.
2. Open the indicator to configure.
3. Click the **Edit** button.
4. Open the **Grade Status** tab.
5. Click **Add a line**.
6. Select the **Grade Type** _(required)_.
7. Select the **Status** _(required)_: **Effective**, **Partial** or **Not Effective**.
8. Click **Save**.

## Post-Condition

- The indicator lists one line with the selected grade type and status.
- Only **Effective** and **Partial** lines open the sub-construct of the indicator as a
  character tag for the learning artifacts of that grade type. A grade type without any
  line leaves the choice of character tags unfiltered.
- Adding a second line for the same grade type is rejected with an error message and the
  line is not saved.
