# Create Distinctive Program Component

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_distinctive_program_component`\
> **Menu:** School > Configuration > Learning Artifact > Program Components\
> **Actor:** user in group `Distinctive Program Component`

## Pre-Condition

- **Data:** The distinctive program exists.
- **Access:** User is in group `Distinctive Program Component`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Program Components** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the component.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Program** _(required)_: Select the distinctive program the component belongs to.
   - **Abbreviation**: Optional short form used in media file names.
4. Click **Save**.

## Post-Condition

- A new component is created and active.
- It becomes selectable in the **Primary Component** and **Secondary Component** fields
  of the learning artifacts of every school unit of the branch of its program.
