# Set Learning Artifact Usage on a Consent Purpose

> **Module:** `ssi_school_learning_artifact`\
> **Extends:** ssi_partner_data_privacy_consent — model `partner_consent_purpose`\
> **Model:** `partner_consent_purpose`\
> **Menu:** Contacts > Configuration > Data Privacy > Consent Purpose\
> **Actor:** user in group `Partner Consent Purpose`\
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The consent purpose already exists.
- **Access:** User is in group `Partner Consent Purpose`.
- **Module:** `ssi_school_learning_artifact` is installed.

## Flow

1. Open the **Contacts > Configuration > Data Privacy > Consent Purpose** menu.
2. Find and open the purpose to map.
3. Click the **Edit** button. **(14.0 only)**
4. Select the **Learning Artifact Usage**:
   - **Inventory**: keeping the artifact in the inventory.
   - **Internal Assessment**: assessing the artifact internally.
   - **Publication**: publishing the artifact.
   - **Promotion**: using the artifact for promotion.
   - Leave it empty for a purpose that does not concern learning artifacts.
5. Click **Save**.

## Post-Condition

- The consents recorded for this purpose now count for the selected usage in the
  **Parental Consent** tab of the learning artifacts.
- Several purposes may share one usage; the latest consent among them decides.
