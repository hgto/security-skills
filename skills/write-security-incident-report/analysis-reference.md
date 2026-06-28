# Analysis Reference — Incident Report Supporting Data

This reference covers the three analytically demanding components of a security incident report: timeline construction, IOC documentation, and MITRE ATT&CK mapping. Use it alongside `incident-report-template.md` and in conjunction with the `security-language` standard.

---

## 1. Timeline Construction

### 1.1 Format Requirements

All times are UTC. State "all times UTC" once at the top of the timeline section and do not repeat it per row. Use ISO 8601 extended format: `2026-06-28T14:32:07Z`. Never use local time, ambiguous offsets, or informal formats such as "3pm" or "Mon afternoon."

### 1.2 Table Structure

| Timestamp (UTC) | Event/Action | Source/Evidence | Actor |
|---|---|---|---|
| 2026-06-28T14:32:07Z | Example: PowerShell process spawned by Word macro | EDR telemetry — host `wkstn-042`, event ID 4688 | Threat actor (assessed) |
| 2026-06-28T15:01:44Z | Example: SOC analyst opened alert in ticketing system | SIEM alert `INC-20260628-001`, ticket timestamp | SOC analyst (role) |

### 1.3 Column Guidance

- **Timestamp (UTC):** Exact timestamp from the source log. If the log is in a non-UTC timezone, convert and note the original timezone in parentheses: `2026-06-28T14:32:07Z (converted from AEST +10)`.
- **Event/Action:** One declarative sentence. Factual for observed events; marked "estimated" for inferred timing. Distinguish two parallel tracks:
  - *Threat actor activity* — actions attributable to the external party based on evidence.
  - *Response activity* — actions taken by defenders, including detection, containment, and recovery steps.
- **Source/Evidence:** The specific artifact, log, or sensor that produced this data point. Name the system, log file, event ID, or document. "EDR" alone is insufficient; "EDR telemetry — host `wkstn-042`, event ID 4688" is sufficient.
- **Actor:** Who performed the action. Use roles, not names (e.g., "SOC analyst," "incident commander," "threat actor"). Mark assessments of threat actor activity as "(assessed)" if the attribution to the external party is inferred rather than directly observed.

### 1.4 Inferred Timing

When the exact time cannot be determined from evidence, note it explicitly:

> `2026-06-28T12:00:00Z (estimated)` — Macro execution inferred to have occurred within two hours prior to first EDR alert; no process-creation log available for this period.

Do not present inferred times as precise facts. Do not omit uncertain events from the timeline — include them with the "(estimated)" marker and explain the basis for the estimate.

### 1.5 Dwell Time, MTTD, and MTTR

Calculate and report these three metrics at the close of the timeline section:

- **Dwell time:** Time from estimated initial access to detection. If initial access time is uncertain, provide a range (minimum and maximum).
- **MTTD (Mean Time to Detect):** Time from the first detectable indicator to the detection event that triggered the response.
- **MTTR (Mean Time to Respond / Recover):** Time from detection to confirmed containment, or to service restoration, as appropriate to the incident type.

Example statement:

> Estimated dwell time: 26–74 hours (minimum from first observed EDR alert; maximum from estimated initial access window). MTTD: 2h 14m (first IOC available 2026-06-26T12:18Z; detection alert fired 2026-06-26T14:32Z). MTTR: 8h 41m (detection to confirmed containment 2026-06-26T23:13Z).

---

## 2. Indicators of Compromise (IOC) Documentation

### 2.1 Defanging Network IOCs

All network IOCs in a written report must be defanged to prevent accidental activation by email clients, browsers, and SIEM platforms that auto-linkify URLs and IP addresses.

| Original | Defanged |
|---|---|
| `http://malicious.example.com/payload` | `hxxp://malicious[.]example[.]com/payload` |
| `https://evil.co/c2` | `hxxps://evil[.]co/c2` |
| `192.168.1.1` | `192.168[.]1[.]1` |
| `10.0.0.50` | `10.0[.]0[.]50` |
| `malware@example.com` | `malware[@]example[.]com` |

Rules:
- Replace `http://` with `hxxp://` and `https://` with `hxxps://`.
- Bracket the dots in domain names: `example[.]com`.
- Bracket the final two octet-separator dots in IP addresses (e.g. `192.168[.]1[.]1`); bracketing all dots is also acceptable.
- Apply defanging even when the IOC appears inside a code block or table cell in a human-readable document.

**Exception:** Defanging is not required in machine-readable appendices (STIX bundles, YARA rules, Sigma rules) because those formats are consumed by parsers, not rendered by human-facing clients. Note this exception explicitly in the appendix heading.

### 2.2 IOC Table Structure

Group IOCs by type. Preferred type order: hashes (SHA-256 preferred over MD5/SHA-1), IP addresses, domains, email addresses, file paths, registry keys, other.

| Type | Indicator | Context | Confidence | First seen (UTC) | Last seen (UTC) | Source |
|---|---|---|---|---|---|---|
| SHA-256 | `a3f1b2c4d5e6...` (64 hex chars) | Dropper binary — `invoice.doc` delivered via phishing | High | 2026-06-28T14:30:00Z | 2026-06-28T14:30:00Z | EDR quarantine log |
| IP address | `198.51.100[.]42` | Command-and-control beacon destination | Moderate | 2026-06-28T14:35:12Z | 2026-06-28T16:22:09Z | Firewall netflow |
| Domain | `updates[.]malicious-cdn[.]com` | C2 callback domain resolved during infection | Moderate | 2026-06-28T14:35:00Z | 2026-06-28T16:00:00Z | DNS query log |
| File path | `C:\Users\Public\svchost32.exe` | Dropped payload — masquerades as system process | High | 2026-06-28T14:33:44Z | 2026-06-28T15:58:01Z | EDR telemetry |
| Registry key | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\WindowsUpdate` | Persistence mechanism — points to dropped binary | High | 2026-06-28T14:34:02Z | 2026-06-28T15:58:05Z | Registry change log |

### 2.3 Confidence Column Values

Use the same confidence scale as the `security-language` standard:

- **High** — IOC observed directly in an artifact from the affected system; corroborated by two or more independent sources.
- **Moderate** — IOC observed in one source with contextual corroboration (e.g., domain resolves to known C2 infrastructure, but no direct connection log from the affected host).
- **Low** — IOC from threat intelligence feed, shared indicator, or extrapolation; not directly observed in the incident evidence.

Avoid marking all IOCs as high confidence. Many IOCs in an incident are moderate or low, and overstating confidence undermines the report's credibility.

### 2.4 Machine-Readable Appendices

For operational consumers (threat intelligence platforms, SIEM, EDR), include machine-readable formats in appendices. Mention their availability in the IOC section body:

> Full IOC set in machine-readable formats is available in Appendix B (STIX 2.1 bundle) and Appendix C (Sigma rules for detection engineering; YARA rules for file-level hunting).

Note that STIX/TAXII is the standard for structured threat intelligence sharing. Sigma rules translate detection logic across SIEM platforms. YARA rules provide file and memory pattern matching for hunting and antivirus use.

---

## 3. MITRE ATT&CK Mapping

### 3.1 Evidence Requirement

Every ATT&CK technique entry must be tied to a specific observed event in the timeline. An ATT&CK technique cited without an evidence anchor is speculation, not analysis. If you cannot point to a log entry, artifact, or forensic finding that supports the technique, do not include it.

### 3.2 Table Structure

| Tactic | Technique ID | Technique Name | Observed behavior / Evidence |
|---|---|---|---|
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | Phishing email with `invoice.doc` attachment received at `user[@]example[.]com` 2026-06-28T14:22:17Z — email gateway log `MSG-20260628-00441` |
| Execution | T1059.001 | Command and Scripting Interpreter: PowerShell | PowerShell process spawned by `WINWORD.EXE` — EDR event ID 4688, host `wkstn-042`, 2026-06-28T14:32:07Z |
| Persistence | T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Registry key `HKCU\...\Run\WindowsUpdate` created — registry change log, host `wkstn-042`, 2026-06-28T14:34:02Z |
| Defense Evasion | T1036.005 | Masquerading: Match Legitimate Name or Location | Dropped binary named `svchost32.exe` placed in `C:\Users\Public\` — EDR telemetry, 2026-06-28T14:33:44Z |
| Collection | T1005 | Data from Local System | File enumeration of `C:\Users\[username]\Documents\` — EDR file access telemetry, 2026-06-28T15:12:30Z |

### 3.3 Technique vs. Sub-technique

Use the most specific identifier available. Prefer sub-techniques (e.g., `T1566.001`) over parent techniques (e.g., `T1566`) when the observed evidence supports the more specific classification. Do not use a sub-technique when the evidence only supports the parent.

### 3.4 What ATT&CK Mapping Is Not

ATT&CK mapping describes *how* the incident unfolded using a shared vocabulary. It does not:

- Identify or attribute the external party.
- Establish motive or intent.
- Confirm or deny any legal conclusion.

Frame ATT&CK entries as behavioral observations, not as characterizations of an actor's identity or objectives. Use the technique name and evidence; avoid editorializing about what the actor "intended" or "wanted to achieve."

### 3.5 Techniques Not Directly Observed

If threat intelligence or external reporting suggests a technique that was not directly observed in your evidence, note it separately with a clear marker:

> **Unconfirmed / intelligence-sourced (not observed in incident evidence):** T1041 — Exfiltration Over C2 Channel. We assess with low confidence that data may have been transferred via the observed C2 channel; no confirmed exfiltration artifact has been identified in forensic review to date.

This distinguishes direct observations from inferred or intelligence-derived assessments.
