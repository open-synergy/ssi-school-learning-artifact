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
   - **Person in Charge**: Optional. Select the user in charge of the content.
   - **Ready**: Check when the content is ready to be distributed.
   - **Date Published**: Optional. Enter the date the content was distributed.
7. Optionally select the **Actual Channels** and write the **Distribution Note** once
   the artifact was distributed outside Odoo.
8. Click **Save**.

## Post-Condition

- The row is listed in the **Production** table with the **Word Count** of its content.
  The word count is informative and never blocks the content.
- Odoo only records the production. The distribution itself happens outside Odoo.
