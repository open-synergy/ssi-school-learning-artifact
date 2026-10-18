# Create Learning Artifact Rubric

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_rubric`\
> **Menu:** School > Configuration > Learning Artifact > Rubrics\
> **Actor:** user in group `Learning Artifact Rubric`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Rubric`.
- **Data:** At least one curation status exists for the **Ethics Fail Status** field
  (see `school_learning_artifact_curation_status/01-create`).

## Flow

1. Open the **School > Configuration > Learning Artifact > Rubrics** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the rubric.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Ethics Fail Status** _(required)_: Select the status given to an artifact that
     fails the ethics gate.
   - **Schools**: Optional. Select the schools that use the rubric. Leave it empty to
     make this the fallback rubric of the schools without a rubric.
   - **Knockout Status**: Optional. Select the status given when an aspect scores at or
     below its knockout score.
   - **Maximum Revision**: Optional. Enter how many times a curated artifact that needs
     revision can be reopened. The default is 1.
   - **Ethics Assessor Groups**, **Require Distinct Assessors**, **Forbid Creator
     Assessment**: Optional. Set who may assess.
   - **Aspects** tab: Optional. Add one line per scored aspect with its code, name,
     score range, knockout score, assessor slot and assessor groups.
   - **Thresholds** tab: Optional. Add one line per minimum total score with the status
     it gives.
4. Click **Save**.

## Post-Condition

- A new rubric is created and active.
- Learning artifacts of the schools it applies to use it when they are created, and get
  one score row per aspect when the curation starts.
