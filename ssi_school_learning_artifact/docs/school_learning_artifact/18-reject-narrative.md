# Reject Showcase Narrative

> **Module:** `ssi_school_learning_artifact`\
> **Model:** `school_learning_artifact`\
> **Menu:** School > Learning Artifacts > Learning Artifacts\
> **Actor:** an approver of the **Standard** approval template of the showcase production\
> **Requires:** `15-request-narrative-approval`

## Pre-Condition

- **Record:** The row of the channel in the **Production** table has **Status**
  **Waiting Approval**.
- **Config:** The **Standard** approval template of the showcase production has at least
  one approver detail.
- **Access:** User is the approver whose turn it is, and can see the artifact.

## Flow

1. Open the **School > Learning Artifacts > Learning Artifacts** menu.
2. Open the curated record.
3. Open the **Showcase** tab.
4. In the **Production** table, find the row of the channel (**Status**: **Waiting
   Approval**).
5. Click the **Reject** button of the row.

## Post-Condition

- The row **Status** is **Rejected**. The coordinator can click **Return** on it (see
  `16-return-narrative`).
- If the user is not an approver whose turn it is, an error message states it and the
  row stays **Waiting Approval**.
