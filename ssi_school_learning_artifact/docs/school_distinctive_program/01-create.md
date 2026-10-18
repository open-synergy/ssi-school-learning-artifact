# Create Distinctive Program

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_distinctive_program`\
> **Menu:** School > Configuration > Learning Artifact > Distinctive Programs\
> **Actor:** user in group `Distinctive Program`

## Pre-Condition

- **Data:** The branch that owns the program exists.
- **Access:** User is in group `Distinctive Program`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Distinctive Programs** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the program.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Branch** _(required)_: Select the branch that owns the program. All school units
     of the branch inherit it.
   - **Abbreviation**: Optional short form of the program name.
   - On the **Components** tab, add one line per component of the program (code, name,
     abbreviation).
4. Click **Save**.

## Post-Condition

- A new program is created and active.
- Its components become selectable in the **Primary Component** and **Secondary
  Component** fields of the learning artifacts of every school unit of the branch.
