# Select Character Indicator of Learning Artifact

> **Module:** `ssi_school_learning_artifact_character`\
> **Model:** `school_learning_artifact`\
> **Extends:** ssi_school_learning_artifact — model `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **State:** Draft\
> **Requires:** `01-create`, `11-tag-character`

## Pre-Condition

- **Record:** Status is **Draft** (a user in group
  `School Learning Artifact — Validator` can also select indicators while the status is
  **Waiting for Approval** or **On Progress**). The **Dominant Character Tag** or the
  **Secondary Character Tag** is filled in (`11-tag-character`).
- **Data:** At least one active **Character Indicator** exists for the dominant or the
  secondary tag (`ssi_school_character/school_character_indicator/01-create`).
- **Config:** When the school filters indicators by grade, the **Grade Status** lines of
  the indicators are set (`school_character_indicator/01-set-grade-status`). A line
  without grades applies to every grade of its grade type; a line with grades applies
  only to those grades. An active `policy.template` for this model grants
  `character_indicator_ok` for the state; the standard template grants it to the group
  `School Learning Artifact — User` in **Draft** and to the group
  `School Learning Artifact — Validator` in **Waiting for Approval** and **On
  Progress**.
- **Access:** User is in group `School Learning Artifact — User` and can see the
  artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to fill in.
3. Click the **Edit** button.
4. Open the **Character Tag** tab.
5. Select the **Character Indicators**. The choice lists the active indicators of an
   active sub-construct; when a status line applies to the grade of the artifact, it
   lists only the indicators that are **Effective** or **Partial** on those lines.
6. Click **Save**.

## Post-Condition

- The selected indicators are saved on the artifact. They are only a mark of the
  activity, not evidence of the character achievement of a student.
- Every selected indicator must belong to the dominant or the secondary tag when one of
  them is filled in; otherwise an error message is shown and nothing is saved.
- Checking **Not Clearly Evident** (`11-tag-character`) empties the indicators;
  selecting indicators on an artifact that is already marked **Not Clearly Evident** is
  rejected with an error message and nothing is saved.
- A user outside the policy sees the field read-only.
