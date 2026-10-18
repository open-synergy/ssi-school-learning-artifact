# Create Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **State:** `—` → `draft`

## Pre-Condition

- **Data:** The school, the academic year and the class of the students exist, and the
  students are registered in the school.
- **Config:** An active `sequence.template` exists for this model, so the artifact code
  is generated when the record is saved.
- **Access:** User is in group `School Learning Artifact — User`.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **School** _(required)_: Select the school unit that owns the artifact. Changing
     the school clears the class, students, learning area, components, dimension and
     phase.
   - **Academic Year** _(required)_: Select the academic year of the activity.
   - **Class** _(required)_: Select a class of the selected school. **Grade** and
     **Grade Type** are filled automatically, read-only, from the class, and **Graduate
     Profile** is filled automatically from the grade.
   - **Activity Name** _(required)_: Enter a short title of the activity.
   - **Media Type** _(required)_: Select **Photo**, **Video** or **Document**.
   - **Date**: Defaults to today. Change if needed.
   - **Students**, **Learning Area**, **Category**, **Description**, **Link**, the
     component, dimension and phase fields and the reflections are optional while the
     artifact is a draft, but most of them are required before it can be submitted (see
     `02-submit`).
4. Click **Save**.

## Post-Condition

- A new record is created in **Draft** status.
- The **Code** of the artifact is generated automatically from the sequence template.
