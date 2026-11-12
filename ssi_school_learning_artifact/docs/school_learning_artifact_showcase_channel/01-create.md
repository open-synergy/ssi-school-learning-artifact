# Create Learning Artifact Showcase Channel

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact_showcase_channel`\
> **Menu:** School > Configuration > Learning Artifact > Showcase Channels\
> **Actor:** user in group `Learning Artifact Showcase Channel`

## Pre-Condition

- **Access:** User is in group `Learning Artifact Showcase Channel`.

## Flow

1. Open the **School > Configuration > Learning Artifact > Showcase Channels** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the channel through which artifacts are
     showcased.
   - **Code** _(required)_: Enter a unique code, or enter **/** to assign it later using
     **Generate Code**.
   - **Schools**: Optional. Select the schools that can use the channel. Leave it empty
     to make the channel available to every school.
   - **Minimum Publication Consent** _(required)_: Leave **Limited** (the default) to
     add no requirement, or select **Full** to accept only the artifacts whose effective
     publication consent is full. A production for this channel is refused for any other
     artifact, and a production that no longer meets the channel is marked as not
     meeting it and loses its **Ready** check.
   - **Content Guideline**: Optional. Enter advice on the content for the channel, for
     example the suggested length of the text. It never blocks the content.
4. Click **Save**.

## Post-Condition

- A new showcase channel is created and active.
- It becomes selectable in the **Planned Channels**, **Actual Channels** and
  **Production** of the curated artifacts of the schools it applies to.
