# Create Learning Artifact Showcase Stage

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_showcase_stage`\
> **Menu:** School > Configuration > Learning Artifact > Showcase Stages\
> **Actor:** user in group `Learning Artifact Showcase Stage`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Showcase Stage`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Showcase Stages** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the stage, as the column of the board.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Sequence**: Enter the order of the stage on the board. The stage with the lowest
     sequence is the first stage given to a curated artifact.
   - **Folded in Board**: Check to fold the column of the stage on the board.
   - **Schools**: Optional. Select the schools that can use the stage. Leave it empty to
     make the stage available to every school.
   - **Require Eligible Curation Status**: Check to let an artifact move into the stage
     only when its curation status is **Eligible**.
   - **Require Publication Consent**: Check to let an artifact move into the stage only
     when the parental consent allows the showcase, following the showcase policy of its
     school.
   - **Allowed Groups**: Optional. Select the groups whose users can move an artifact
     into the stage. Leave it empty to let anyone who may edit the artifact do it.
4. Click **Save**.

## Post-Condition

- A new showcase stage is created and active.
- It becomes a column of the showcase board and is selectable in the **Showcase Stage**
  field of the curated artifacts of the schools it applies to.
