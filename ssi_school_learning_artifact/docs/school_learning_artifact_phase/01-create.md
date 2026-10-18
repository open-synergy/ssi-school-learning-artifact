# Create Learning Artifact Phase

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_phase`\
> **Menu:** School > Configuration > Learning Artifact > Phases\
> **Actor:** user in group `Learning Artifact Phase`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Phase`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Phases** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the phase.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Schools**: Optional. Select the schools that can use the phase. Leave it empty to
     make the phase available to every school.
4. Click **Save**.

## Post-Condition

- A new phase is created and active.
- It becomes selectable in the **Phase** field of the learning artifacts of the schools
  it applies to.
