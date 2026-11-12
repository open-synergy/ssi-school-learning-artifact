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
   - **Require Distinct Assessors**, **Forbid Creator Assessment**: Optional. Set who
     may assess. The ethics gate aspects count in the assessor slot they are set to.
   - **Aspects** tab: Optional. Add the aspects. Repeat the following steps as many
     times as needed:
     - Click **Add a line**.
     - Fill in the dialog with:
       - **Code** _(required)_: Enter the short code of the aspect.
       - **Name** _(required)_: Enter the name of the aspect.
       - **Aspect Type** _(required)_: Select **Scored Aspect** or **Ethics Gate**.
       - **Gate Source**: Ethics gate aspects only. Leave **Manual** to let the assessor
         pick the level, or select **Inventory Consent** to let the system fill the
         level from the inventory consent of the students (a full or limited consent
         gives a passing level, any other gives a failing level). The aspect then needs
         at least one level that fails the gate and one that does not.
       - **Knockout Score**: Optional, scored aspects only. A score at or below it
         knocks the artifact out.
       - **Assessor Slot** _(required)_: Select the primary or the secondary assessor.
       - **Assessor Groups**: Optional. Select the groups allowed to assess the aspect.
       - **Levels**: Add the levels that the assessor can pick. Repeat the following
         steps as many times as needed:
         - Click **Add a line**.
         - Fill in each line with:
           - **Description** _(required)_: Enter the full text of the level.
           - **Score**: Enter the score of the level (scored aspects only). The score
             range of the aspect follows its levels.
           - **Fails the Gate**: Check it for the answer that fails the gate (ethics
             gate aspects only).
     - Click **Save** on the dialog. The curation needs at least one ethics gate aspect.
   - **Thresholds** tab: Optional. Add one line per minimum total score with the status
     it gives.
4. Click **Save**.

## Post-Condition

- A new rubric is created and active.
- Learning artifacts of the schools it applies to use it when they are created, and get
  one row per aspect when the curation starts: the ethics gate aspects in its **Ethics
  Gate** table and the scored aspects in its **Artifact Assessment** table.
