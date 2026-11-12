# Record Showcase Production of Learning Artifact

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** user in group `School Learning Artifact — User`\
> **Requires:** `06-curate`

## Pre-Condition

- **Record:** Status is **Curated**.
- **Config:** A showcase channel that applies to the school exists (see
  `school_learning_artifact_showcase_channel/01-create`).
- **Access:** User is in group `School Learning Artifact — User` and can see the
  artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Click the **Edit** button.
4. Open the **Showcase** tab.
5. Optionally select the **Planned Channels** of the showcase.
6. In the **Production** table, click **Add a line** and fill in the row:
   - **Channel** _(required)_: Select the channel the content is produced for.
   - **Content**: Enter the text produced for the channel.
   - **Person in Charge**: Optional while the row is **Draft**. Select the user in
     charge of the content. It becomes the teacher of the artifact when the row is
     returned to the teacher.
   - **Ready**: Read-only until the narrative is **Approved**. Check it when the content
     is ready to be distributed.
   - **Date Published**: Optional. Enter the date the content was distributed.
7. Optionally select the **Actual Channels** and write the **Distribution Note** once
   the artifact was distributed outside Odoo.
8. Click **Save**.

## Post-Condition

- The row is listed in the **Production** table with **Status** **Draft** and the **Word
  Count** of its content. The narrative then goes through the workflow:
  `13-return-narrative-to-teacher`, `14-submit-narrative`,
  `15-request-narrative-approval`, `16-return-narrative`, `17-approve-narrative` and
  `18-reject-narrative`.
- **Ready** can be checked only on an **Approved** row; checking it on any other status
  is refused with an error message. The **Word Count** blocks the **Submit** of the
  narrative outside the word limits of the channel.
- Odoo only records the production. The distribution itself happens outside Odoo.
