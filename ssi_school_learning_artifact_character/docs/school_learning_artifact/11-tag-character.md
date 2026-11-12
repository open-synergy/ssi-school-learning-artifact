# Tag Character of Learning Artifact

> **Module:** `ssi_school_learning_artifact_character`\
> **Model:** `school_learning_artifact`\
> **Extends:** ssi_school_learning_artifact — model `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — Validator`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**, **Waiting for Approval** or **On Progress**.
- **Data:** At least one active **Character Sub-construct** exists
  (`ssi_school_character/school_character_subconstruct/01-create`).
- **Config:** An active `policy.template` for this model grants `character_tag_ok` for
  these states to the group of the actor. The standard template grants it to the group
  `School Learning Artifact — Validator`.
- **Access:** User is in group `School Learning Artifact — Validator` and can see the
  artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the record to tag.
3. Click the **Edit** button.
4. Open the **Character Tag** tab.
5. Select the **Dominant Character Tags**. You can select more than one; there is no
   limit. The choice lists the active sub-constructs; when the grade type of the
   artifact has indicator statuses, it lists only the sub-constructs with an
   **Effective** or **Partial** indicator at that grade type. The **Dominant Character
   Tag Codes** field shows the codes of the selected tags and cannot be edited.
6. Optionally select the **Secondary Character Tags** in the same way. A sub-construct
   cannot be both a dominant and a secondary tag. The **Secondary Character Tag Codes**
   field shows the codes of the selected tags and cannot be edited. Check **Not Clearly
   Evident** instead when no sub-construct is clearly evident; the **Dominant Character
   Tags**, the **Secondary Character Tags**, the **Dominant Character Indicators** and
   the **Secondary Character Indicators** are emptied at once.
7. Click **Save**.

## Post-Condition

- The selected character tags are saved on the artifact. The tags are only a mark of the
  activity, not evidence of the character achievement of a student.
- The tags can be saved whatever the assessment consent of the students is.
- The tag codes are shown in the **Dominant Character Tag Codes** and **Secondary
  Character Tag Codes** fields, separated by commas.
- A sub-construct selected as both a dominant and a secondary tag is rejected with an
  error message and nothing is saved.
- Checking **Not Clearly Evident** empties the dominant tags, the secondary tags and all
  the character indicators, also when they were sent together with the check; no error
  message is shown. Unchecking it does not bring them back.
- Adding a dominant tag to an artifact that is already marked **Not Clearly Evident** is
  rejected with an error message and nothing is saved.
- A user outside the policy sees the tag fields and the **Not Clearly Evident** check
  read-only.
