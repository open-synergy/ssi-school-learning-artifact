# Select Learning Artifact for Showcase

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** Status is **Curated**. The artifact already has the first showcase stage,
  given automatically when it was curated.
- **Config:** A showcase stage that applies to the school exists (see
  `school_learning_artifact_showcase_stage/01-create`).
- **Access:** User is in group `School Learning Artifact — User` and can see the
  artifact. When the target stage lists allowed groups, the user is in one of them.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Click the **Edit** button.
4. Open the **Showcase** tab.
5. Select the **Showcase Stage** the artifact moves into.
6. Click **Save**.

The same move can be done by dragging the card of the artifact to another column of the
board in **School > Learning Artifacts > Showcase**.

## Post-Condition

- The artifact is in the selected stage, and the move is logged in the chatter with the
  user and the time.
- If the artifact does not meet a requirement of the stage (the curation status is not
  **Eligible**, the parental consent does not allow the showcase, or the user is outside
  the allowed groups), an error message states the problem and the stage does not
  change.
