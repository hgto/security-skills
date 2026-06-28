# Security Incident Report — Template

> **How to use this template:** Copy this file. Fill every `[REQUIRED]` field. Replace every `[OPTIONAL — remove if not applicable]` placeholder with content or delete the line. Do not deliver a report with unfilled placeholders. Before delivery, run `verify-security-language` on the completed draft.

---

## Metadata

| Field | Value |
|---|---|
| **Report ID** | [REQUIRED — e.g., INC-2026-0042] |
| **TLP Classification** | [REQUIRED — TLP:RED / TLP:AMBER+STRICT / TLP:AMBER / TLP:GREEN / TLP:CLEAR] |
| **Author** | [REQUIRED — role, not name; e.g., "Lead Incident Analyst, Security Operations"] |
| **Date** | [REQUIRED — ISO 8601: 2026-06-28] |
| **Version** | [REQUIRED — e.g., 1.0] |
| **Status** | [REQUIRED — DRAFT / FINAL] |
| **Distribution** | [REQUIRED — list roles or groups; do not list names; consistent with TLP classification] |
| **Reviewed by** | [OPTIONAL — role of reviewer, date of review] |

---

## Executive Summary

> **Audience:** Non-technical leadership, legal, and communications. Avoid technical jargon. Do not include raw IOCs, log excerpts, or MITRE technique IDs in this section. Use plain language.

[REQUIRED — 3–5 sentences covering: what happened (in plain terms), when it was detected, what systems or data were affected, what response actions were taken, and the current status. Do not assert exfiltration as confirmed fact unless forensics has confirmed it. Do not assert a compliance outcome — flag it for counsel/compliance review if applicable.]

---

## Incident Overview / Classification

| Field | Value |
|---|---|
| **Incident type** | [REQUIRED — e.g., phishing, credential compromise, ransomware, insider activity, data exposure] |
| **Severity** | [REQUIRED — Critical / High / Medium / Low — justify briefly; e.g., "High: single host, data accessed but not confirmed exfiltrated"] |
| **Detection source** | [REQUIRED — e.g., EDR alert, SIEM correlation rule, user report, external notification] |
| **Date/time first detected** | [REQUIRED — ISO 8601 UTC: 2026-06-28T14:32:07Z] |
| **Date/time reported** | [REQUIRED — ISO 8601 UTC] |
| **Date/time contained** | [REQUIRED if applicable — ISO 8601 UTC; "Ongoing" if containment not yet achieved] |
| **Date/time closed** | [OPTIONAL — ISO 8601 UTC; leave blank if open] |
| **Incident commander** | [REQUIRED — role, not name] |
| **Ticket / tracking ID** | [OPTIONAL — link to incident ticket] |

---

## Timeline

> All times UTC. Use ISO 8601 format: `2026-06-28T14:32:07Z`. Mark inferred times as `(estimated)`. Distinguish threat actor activity from response activity in the Event/Action column.

| Timestamp (UTC) | Event/Action | Source/Evidence | Actor |
|---|---|---|---|
| [ISO 8601 UTC] | [Declarative sentence — fact or "(estimated)" if inferred] | [Specific log, artifact, or sensor — include system name, log type, event ID] | [Role — e.g., "threat actor (assessed)", "SOC analyst", "incident commander"] |

> **Dwell time:** [REQUIRED if calculable — e.g., "26–74 hours (minimum from first EDR alert; maximum from estimated initial access window)"]
> **MTTD:** [REQUIRED — time from first available indicator to detection]
> **MTTR:** [REQUIRED — time from detection to confirmed containment or service restoration]

See `analysis-reference.md` § 1 for detailed timeline construction guidance, including inferred-timing conventions and how to distinguish threat actor vs. response tracks.

---

## Technical Detail / Root Cause

> Describe the technical sequence of events: how initial access was gained, how the activity propagated, and what the root cause is assessed to be. Separate observed facts from assessments. Use the fact/assessment discipline from `security-language`.

### Initial Access

[REQUIRED — how the external party or internal actor first gained access. State whether authentication succeeded or failed, and whether the actor held authorization for the resource accessed. Do not write "unauthorized access" — state the authentication and authorization status explicitly.]

### Activity Sequence

[REQUIRED — what happened after initial access: execution, persistence, lateral movement, collection, etc. Each action should correspond to a timeline entry and, where evidence supports it, an ATT&CK technique. Use the passive voice or system-level framing where appropriate.]

### Root Cause

[REQUIRED — the underlying condition that made the incident possible: a misconfiguration, a missing control, a process gap, or a social engineering technique that exploited a user. Frame at the system/process level. Do not assign individual blame.]

> **Assessment:** [OPTIONAL — if the root cause is assessed rather than confirmed, use calibrated language: "We assess with [confidence] confidence that the root cause was likely [condition], based on [evidence]."]

---

## Impact and Scope

> Apply precision to scope claims. Where scope is unknown, state visibility limits explicitly rather than claiming no impact beyond what was investigated.

### Systems

| Category | Systems / Assets |
|---|---|
| **Confirmed affected** | [List hostnames/IDs; mark "none identified" if applicable] |
| **Potentially exposed** | [List systems in scope of investigation but not yet confirmed; note investigation status] |
| **Cleared** | [List systems investigated and found not to have been affected, with basis for clearance] |

> If investigation scope does not cover all potentially relevant systems, state that explicitly: "The following systems were not within the investigation scope and cannot be assessed at this time: [list]."

### Data

State each category separately. Do not conflate data that was accessed in place with data that was confirmed to have left the environment.

| Category | Description |
|---|---|
| **Accessed** | [Data that the activity touched or read, confirmed by log evidence — e.g., "4,200 rows of the `customers` table queried by service account `svc-reporting`"] |
| **Exfiltrated** | [Data confirmed to have left the environment, with the forensic artifact that confirms it — e.g., "None confirmed at this time" or "38 MB transferred to `198.51.100[.]42` per firewall netflow"] |
| **At risk** | [Data co-located with affected systems that could have been accessed but has not been confirmed as accessed or exfiltrated — note visibility limits] |

> If exfiltration cannot be confirmed or ruled out, state: "We assess with [confidence] confidence that data [likelihood term] left the environment; [basis for assessment]. Full confirmation requires [additional forensic step]."

### Business Impact

[REQUIRED — describe operational, financial, or reputational consequences observed or assessed. Quantify where possible: service availability, affected user count, estimated downtime.]

### Regulatory and Legal Implications

[OPTIONAL — if applicable, use the following form:]

> [Data type] was [accessed / potentially exposed] in this incident. This may have implications under [GDPR / HIPAA / state notification law / other framework] — recommend review by compliance/counsel to determine notification obligations and regulatory reporting requirements.

Do not assert that a regulation was violated or that the organization is non-compliant. That determination belongs to legal and compliance teams.

---

## Indicators of Compromise

> All network IOCs are defanged. See `analysis-reference.md` § 2 for defanging rules and confidence definitions. Machine-readable formats are in the appendices.

| Type | Indicator | Context | Confidence | First seen (UTC) | Last seen (UTC) | Source |
|---|---|---|---|---|---|---|
| [SHA-256 / IP address / Domain / Email / File path / Registry key] | [Defanged value] | [What this indicator represents] | [High / Moderate / Low] | [ISO 8601 UTC] | [ISO 8601 UTC] | [Log or artifact name] |

---

## MITRE ATT&CK Mapping

> Each technique must be anchored to a specific observed event. Do not include techniques inferred from external intelligence without marking them as unconfirmed. See `analysis-reference.md` § 3 for mapping guidance.

| Tactic | Technique ID | Technique Name | Observed behavior / Evidence |
|---|---|---|---|
| [Tactic name] | [T####.###] | [Technique name] | [One-sentence description of what was observed, with evidence source and timestamp] |

> **Unconfirmed / intelligence-sourced (not observed in incident evidence):**
> [OPTIONAL — list techniques suggested by threat intelligence but not directly observed, with confidence and likelihood qualifiers]

---

## Response Actions

> Structure by PICERL phase. Record who took which action and when. Use roles, not names.

### Preparation

[OPTIONAL — controls, playbooks, or detection capabilities that were in place and relevant to this incident]

### Identification

[REQUIRED — how and when the incident was identified; what triggered the investigation; initial scoping steps taken]

| Action | Responsible role | Timestamp (UTC) | Outcome |
|---|---|---|---|
| [Action taken] | [Role] | [ISO 8601 UTC] | [Result] |

### Containment

[REQUIRED — steps taken to limit the spread or impact of the incident]

| Action | Responsible role | Timestamp (UTC) | Outcome |
|---|---|---|---|
| [Action taken] | [Role] | [ISO 8601 UTC] | [Result] |

### Eradication

[REQUIRED — steps taken to remove the threat from the environment]

| Action | Responsible role | Timestamp (UTC) | Outcome |
|---|---|---|---|
| [Action taken] | [Role] | [ISO 8601 UTC] | [Result] |

### Recovery

[REQUIRED — steps taken to restore systems and verify clean state]

| Action | Responsible role | Timestamp (UTC) | Outcome |
|---|---|---|---|
| [Action taken] | [Role] | [ISO 8601 UTC] | [Result] |

### Lessons Learned

> See the dedicated Lessons Learned section below.

---

## Lessons Learned

> Blameless. Attribute findings to systems, processes, and controls — not to individuals or teams. Frame deficiencies forward.

### What Went Well

[REQUIRED — at least one item. Acknowledge controls, processes, or responses that functioned as intended.]

- [Example: "EDR telemetry provided sufficient signal to reconstruct the full activity sequence on the affected host."]

### Areas for Improvement

[REQUIRED — specific, process-level observations. Frame as: "The [process / control / configuration] did not [expected behavior]," not "the [team] failed to [action]."]

- [Example: "The alerting configuration did not produce a notification within the detection window; the relevant SIEM rule lacked a tuned threshold for the volume observed."]

### Corrective Actions

| Action | Owner (role) | Due date | Priority |
|---|---|---|---|
| [Specific, actionable corrective action] | [Role responsible for delivery] | [ISO 8601 date: 2026-07-15] | [Critical / High / Medium / Low] |

> Every corrective action must have an owner (by role) and a due date. Actions without owners or deadlines are not actionable and should not appear in this table.

---

## Appendices

### Appendix A — Evidence Inventory

[OPTIONAL — list of forensic artifacts, log extracts, disk images, memory captures, or other evidence collected during the investigation. Include hash values for integrity verification.]

| Artifact | Hash (SHA-256) | Date collected (UTC) | Collected by (role) | Location / custody |
|---|---|---|---|---|
| [Artifact name] | [Hash] | [ISO 8601 UTC] | [Role] | [Storage location or chain-of-custody reference] |

### Appendix B — STIX 2.1 Bundle

[OPTIONAL — machine-readable IOC bundle. IOCs in this appendix are not defanged; this file is intended for machine consumption only.]

```json
{
  "type": "bundle",
  "id": "bundle--[uuid]",
  "objects": []
}
```

### Appendix C — Detection Rules

[OPTIONAL — Sigma rules and/or YARA rules for detection engineering use. IOCs in this appendix are not defanged; these rules are intended for machine consumption only.]

```yaml
# Sigma rule placeholder
title: [Rule title]
status: experimental
```

### Appendix D — Additional Technical Detail

[OPTIONAL — memory forensics output, network packet captures, malware analysis summaries, or other detailed technical content too lengthy for the main report body]
