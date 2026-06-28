# security-skills Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code plugin of five intent-triggered skills for security report writing: a central language standard, a language verifier (with script), and three document-writing skills (findings, incident reports, executive summaries).

**Architecture:** Standard Claude Code plugin — `.claude-plugin/plugin.json` manifest plus a `skills/` directory, one folder per skill, each with a `SKILL.md` and supporting reference/template files. The three document skills and the verifier all cross-reference the central `security-language` skill by name (`**REQUIRED SUB-SKILL:**`), never `@`-links. One Python script (`verify-language.py`) provides mechanical lint detection and is built with TDD.

**Tech Stack:** Markdown (SKILL.md + references/templates), Python 3 stdlib only (`verify-language.py`, tested with `pytest`), YAML frontmatter.

## Global Constraints

- Plugin name: `security-skills`. Repo to be renamed `security-writing` → `security-skills`.
- General-purpose, vendor-neutral. Cite only public standards (NIST, OWASP, MITRE, CISA, FIRST/CVSS, ODNI ICD 203). No org-specific names, scales, or distribution lists.
- The five skill names (final): `security-language`, `verify-security-language`, `write-security-finding`, `write-security-incident-report`, `write-security-executive-summary`.
- Every skill `description` MUST begin with `(hgto/security-skills) ` then `Use when …`.
- Skill `name` frontmatter: letters/numbers/hyphens only. `description`: third person, triggers only — NEVER summarize the skill's workflow.
- Cross-reference other skills by name with `**REQUIRED SUB-SKILL:**`; never use `@`-links.
- No slash commands. No CI integration. Python: stdlib only, no third-party deps.
- Skill discipline (writing-skills Iron Law): for the two discipline skills, run a baseline (RED) subagent test BEFORE writing the skill and capture verbatim rationalizations; verify (GREEN) after.
- Frontmatter max 1024 chars. Keep each SKILL.md focused; push heavy reference (tables) into supporting files.

---

### Task 1: Plugin scaffold and manifest

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `README.md`
- Create: `.gitignore`

**Interfaces:**
- Produces: the plugin manifest and directory root that all skills live under (`skills/`).

- [ ] **Step 1: Create the manifest**

`.claude-plugin/plugin.json`:
```json
{
  "name": "security-skills",
  "version": "0.1.0",
  "description": "Skills for writing security findings, incident reports, and executive summaries in neutral, defensible language.",
  "author": { "name": "hgto" }
}
```

- [ ] **Step 2: Create `.gitignore`**

```
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
```

- [ ] **Step 3: Create the README skeleton**

`README.md` with: title `# security-skills`, one-paragraph summary, a "Skills" section listing all five with one-line descriptions (placeholder one-liners acceptable here — finalized in Task 8), and an "Install" section (`/plugin` marketplace install or clone into a plugins dir). Mark the skills list with `<!-- finalized in Task 8 -->`.

- [ ] **Step 4: Verify structure**

Run: `test -f .claude-plugin/plugin.json && python3 -c "import json;json.load(open('.claude-plugin/plugin.json'))" && echo OK`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json README.md .gitignore
git commit -m "feat: scaffold security-skills plugin"
```

---

### Task 2: `security-language` skill (central discipline skill)

**Files:**
- Create: `skills/security-language/SKILL.md`
- Create: `skills/security-language/word-substitutions.md`
- Create: `skills/security-language/estimative-language.md`

**Interfaces:**
- Produces: the canonical word-substitution table (consumed by `verify-language.py` in Task 3 and the verifier skill in Task 4), and the fact-vs-assessment / likelihood-vs-confidence standard referenced by all document skills.

- [ ] **Step 1: RED — baseline test (no skill yet)**

Dispatch a subagent with this prompt and record its output verbatim:
> "Write a 4-sentence summary of this event: someone outside the company got into our email server last night, grabbed customer data, and it's a disaster. Be professional."

Expected baseline failure: uses "attacker"/"hacker", "breach"/"stole", "disaster", states unconfirmed exfiltration as fact, no confidence qualifiers. Capture the exact loaded words used — these seed the rationalization table and the linter term list.

- [ ] **Step 2: Write `word-substitutions.md`**

A heavy-reference table. Columns: `Avoid | Use instead | Why | Legal term of art?`. Include at minimum these rows (verbatim values):

| Avoid | Use instead | Why | Legal term? |
|---|---|---|---|
| attacker | external party, threat actor, unauthorized user | presumes hostile intent + attribution | no |
| hacker | threat actor, unauthorized party | pejorative, imprecise | no |
| victim | affected party, impacted organization | frames legal posture; emotive | no |
| breach | incident, event, unauthorized access | regulatory term of art; triggers duties | YES — escalate to counsel |
| compromised (unconfirmed) | potentially affected, exposed to, accessed by | implies confirmed control | no |
| stolen / exfiltrated (unconfirmed) | accessed, transferred, copied, observed leaving | theft is a legal conclusion | YES — escalate to counsel |
| malicious | unauthorized, anomalous, unexpected | intent claim, often unprovable | no |
| hacked | accessed without authorization | imprecise, sensational | no |
| negligent / careless / sloppy | did not align with [policy/standard], deviated from | blame + liability term | YES — escalate to counsel |
| obviously / clearly / of course | (delete; state the evidence) | asserts conclusion without support | no |
| catastrophic / devastating / massive | significant, material, [quantified] | hyperbole | no |
| destroyed / wiped | rendered unavailable, deleted, encrypted | be precise about observed effect | no |
| backdoor | undocumented access mechanism | loaded; presumes intent | no |
| weaponized | configured to exploit, used to deliver | militarized framing | no |
| guilty / culprit / perpetrator | responsible party, actor, source | criminal-law conclusion | no |
| spy / espionage (unconfirmed) | unauthorized collection of information | geopolitical conclusion | no |
| war / campaign (casual) | sustained activity, related set of events | reserve for evidenced usage | no |
| should have / failed to (personal) | (reframe to system/process) | personal blame; discoverable | no |

Add an **Absolutes blocklist** subsection: `unhackable`, `100% secure`, `fully secure`, `fully eliminated`, `completely eliminated`, `guaranteed`, `impossible`, `cannot be breached`. Note: replace with "reduces the likelihood of", "mitigates", "no evidence of X was found".

- [ ] **Step 3: Write `estimative-language.md`**

Two-axis reference (per ODNI ICD 203):
- **Likelihood (Words of Estimative Probability):** almost no chance/remote (01–05%); very unlikely (05–20%); unlikely (20–45%); roughly even chance (45–55%); likely/probable (55–80%); very likely (80–95%); almost certain (95–99%). Table form.
- **Confidence (sourcing quality, separate axis):** low / moderate / high — quantity, quality, and corroboration of sources. NOT the same as likelihood.
- Canonical combined form: "We assess with moderate confidence that the actor almost certainly exfiltrated the database." Rule: never collapse the two axes into one term; define the scale once per report.
- "No evidence of X" ≠ "X did not happen" — state visibility limits.

- [ ] **Step 4: Write `SKILL.md`**

Frontmatter:
```yaml
---
name: security-language
description: (hgto/security-skills) Use when writing or editing any security report, finding, incident report, or executive summary, or when choosing how to describe an external party, an incident, attribution, or uncertain events in security prose.
---
```
Body sections (concise; push tables to the two reference files):
1. **Overview** — core principle: every assertion is traceable to evidence; separate observed fact from assessment; neutral, defensible, non-blaming language.
2. **The load-bearing rule** — Fact (observed, sourced, past tense, declarative) vs. Assessment (hedged, confidence-qualified). One example pair.
3. **Word choice** — "Use neutral terms; see `word-substitutions.md` for the full table." State the headline rule: "external party"/"threat actor", never "attacker"; never assert "breach"/"stolen" (legal terms) until confirmed.
4. **Likelihood vs. confidence** — two separate axes; pointer to `estimative-language.md`.
5. **Attribution caution** — default "unattributed"; describe TTPs not identity.
6. **Blameless tone** — systems/process not people; roles not names; forward-looking.
7. **Red Flags — STOP** list: "I wrote 'attacker'", "I stated exfiltration without saying 'assessed'", "I used an absolute", "I named/blamed a person", "I called it a 'breach' before confirmation".
8. **Rationalization table** — seeded from Step 1 baseline (e.g. "'Attacker' is just clearer" → "Clarity doesn't require an intent+attribution claim; 'external party' is equally clear and defensible"). Add rows for every rationalization the baseline subagent produced.

- [ ] **Step 5: GREEN — verify with skill**

Dispatch a fresh subagent given the SKILL.md + two reference files as context, same prompt as Step 1. Expected: uses "external party", "incident"/"accessed", confidence-qualified ("assessed … likely"), no absolutes, no blame. If it still violates, add a rationalization-table row / red flag and re-test.

- [ ] **Step 6: Commit**

```bash
git add skills/security-language/
git commit -m "feat: add security-language standard skill"
```

---

### Task 3: `verify-language.py` linter (TDD, Python stdlib)

**Files:**
- Create: `skills/verify-security-language/verify-language.py`
- Test: `skills/verify-security-language/test_verify_language.py`

**Interfaces:**
- Produces: CLI `python3 verify-language.py <file>` (or stdin). For each hit prints `LINE:COL [category] "term" → suggestion`. Exit code 1 if any hits, 0 if clean. Categories: `loaded-term`, `absolute`, `hyperbole`, `legal-term`, `second-person-blame`. A `--json` flag emits a JSON array of `{line, col, category, term, suggestion}`.
- Consumes: the term list mirrors `word-substitutions.md` from Task 2 (keep the mapping in a module-level dict).

- [ ] **Step 1: Write failing tests**

`test_verify_language.py`:
```python
import subprocess, sys, json, pathlib
SCRIPT = pathlib.Path(__file__).parent / "verify-language.py"

def run(text, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          input=text, capture_output=True, text=True)

def test_flags_attacker():
    r = run("The attacker logged in.")
    assert r.returncode == 1
    assert "attacker" in r.stdout
    assert "external party" in r.stdout
    assert "loaded-term" in r.stdout

def test_flags_absolute():
    r = run("The system is now unhackable.")
    assert r.returncode == 1
    assert "absolute" in r.stdout

def test_flags_legal_term():
    r = run("This was a breach.")
    assert "legal-term" in r.stdout

def test_flags_second_person_blame():
    r = run("You failed to apply the patch.")
    assert "second-person-blame" in r.stdout

def test_clean_text_exit_zero():
    r = run("An external party accessed the host; data was observed transferring out.")
    assert r.returncode == 0

def test_case_insensitive():
    assert run("The ATTACKER struck.").returncode == 1

def test_word_boundary_no_false_positive():
    # "war" must not match inside "warehouse" / "aware"
    assert run("The aware warehouse team responded.").returncode == 0

def test_json_output():
    r = run("The attacker won.", "--json")
    data = json.loads(r.stdout)
    assert data[0]["category"] == "loaded-term"
    assert data[0]["term"].lower() == "attacker"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd skills/verify-security-language && python3 -m pytest test_verify_language.py -v`
Expected: FAIL (script not found / no output).

- [ ] **Step 3: Implement `verify-language.py`**

Implement with stdlib only:
- Module-level dicts: `LOADED = {"attacker": "external party / threat actor", "hacker": "threat actor", "victim": "affected party", "malicious": "unauthorized / anomalous", "hacked": "accessed without authorization", "backdoor": "undocumented access mechanism", ...}`, `LEGAL = {"breach": "incident / unauthorized access", "stolen": "accessed / transferred", "exfiltrated": "observed transferring", "negligent": "did not align with policy", "compromised": "potentially affected"}`, `HYPERBOLE = {"catastrophic","devastating","massive","disaster","obviously","clearly"}`, `ABSOLUTES = {"unhackable","100% secure","fully secure","guaranteed","impossible","fully eliminated"}`, and a regex for second-person blame: `\byou (failed|should have|neglected|forgot)\b`.
- Match each term with `re.finditer(r"\b" + re.escape(term) + r"\b", line, re.IGNORECASE)` for word-boundary safety (covers `test_word_boundary_no_false_positive`). For multi-word absolutes, match the phrase directly.
- For each hit collect `{line, col, category, term, suggestion}`.
- Read from file arg if given, else stdin. `--json` → `print(json.dumps(hits))`; else human lines `f'{line}:{col} [{category}] "{term}" → {suggestion}'`.
- `sys.exit(1 if hits else 0)`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd skills/verify-security-language && python3 -m pytest test_verify_language.py -v`
Expected: PASS (8 passed).

- [ ] **Step 5: Commit**

```bash
git add skills/verify-security-language/verify-language.py skills/verify-security-language/test_verify_language.py
git commit -m "feat: add verify-language.py linter with tests"
```

---

### Task 4: `verify-security-language` skill

**Files:**
- Create: `skills/verify-security-language/SKILL.md`

**Interfaces:**
- Consumes: `verify-language.py` (Task 3); `security-language` word table (Task 2).
- Produces: a re-framing procedure invoked standalone and as the final step of Tasks 5–7.

- [ ] **Step 1: RED — baseline test**

Dispatch a subagent (no skill): "Rewrite this to be clinical and neutral: 'The hacker obviously broke into our server and stole all our customer data. It was a catastrophic breach and the ops team totally dropped the ball.'" Record output. Expected baseline failure: partial neutralization, keeps some loaded terms, doesn't separate fact from assessment, doesn't add confidence qualifiers, no systematic check.

- [ ] **Step 2: Write `SKILL.md`**

Frontmatter:
```yaml
---
name: verify-security-language
description: (hgto/security-skills) Use when reviewing, checking, or cleaning up a security draft for loaded or non-neutral language, or when asked to make security writing clinical, neutral, or defensible before it is delivered.
---
```
Body:
1. **Overview** — applies the `security-language` standard to an existing draft: mechanical detection by script, clinical re-framing by judgment.
2. **Procedure** (numbered): (a) run `python3 verify-language.py <draft>` (or pipe via stdin); (b) triage every hit; (c) reframe loaded terms using the substitution table; (d) demote any unsourced claim to an assessment with explicit likelihood + confidence; (e) strip absolutes and hyperbole; (f) de-personalize blame (systems/process, roles not names); (g) re-run the script and confirm exit 0 before delivering.
3. **What the script cannot catch** (do by hand): fact-vs-assessment separation, missing confidence qualifiers, premature attribution, hindsight bias. The script is necessary, not sufficient.
4. **`**REQUIRED SUB-SKILL:** security-language`** for the rules behind each rewrite.
5. **Example** — before/after using the Step 1 prompt text, showing the clinical rewrite with confidence qualifiers.

- [ ] **Step 3: GREEN — verify**

Dispatch fresh subagent with SKILL.md + script as context, same Step 1 prompt. Expected: runs (or references running) the script, produces fully neutral clinical text with fact/assessment separation and confidence qualifiers, no blame. Adjust and re-test if not.

- [ ] **Step 4: Commit**

```bash
git add skills/verify-security-language/SKILL.md
git commit -m "feat: add verify-security-language skill"
```

---

### Task 5: `write-security-finding` skill

**Files:**
- Create: `skills/write-security-finding/SKILL.md`
- Create: `skills/write-security-finding/finding-template.md`
- Create: `skills/write-security-finding/severity-rating.md`

**Interfaces:**
- Consumes: `security-language` (Task 2), `verify-security-language` (Task 4).
- Produces: a finding write-up structure + template.

- [ ] **Step 1: Write `severity-rating.md`**

Reference: CVSS bands (None 0.0 / Low 0.1–3.9 / Medium 4.0–6.9 / High 7.0–8.9 / Critical 9.0–10.0); note v3.1 vs v4.0 (v4.0 removed Scope → Vulnerable/Subsequent System; added Attack Requirements; nomenclature CVSS-B/BT/BTE); record the full **vector string**, not just the number. OWASP Risk Rating (Likelihood × Impact, each averaged 0–9, Low/Med/High buckets, 3×3 matrix). Rule: justify every rating with a vector or factor table + a one-sentence reconciliation with business/environmental context. Mention EPSS/SSVC as complements, DREAD as deprecated.

- [ ] **Step 2: Write `finding-template.md`**

Copy-paste skeleton with these headed fields: `Finding ID`, `Title` (name the vulnerability, not the symptom), `Severity` (label + CVSS vector or OWASP factors), `Affected Assets` (precise: host/URL/param/version), `Description` (root cause/mechanism), `Impact` (business + technical "so what"), `Likelihood/Exploitability`, `Evidence / PoC` (reproducible, redacted, non-destructive — numbered repro steps), `Remediation` (actionable, specific, root-cause-oriented; short-term vs durable), `References` (CWE, OWASP, CVE), `Status`.

- [ ] **Step 3: Write `SKILL.md`**

Frontmatter:
```yaml
---
name: write-security-finding
description: (hgto/security-skills) Use when writing up a security finding, vulnerability, pentest result, code-review issue, or audit observation, or when documenting a single discovered weakness with its severity, impact, evidence, and remediation.
---
```
Body: overview (the Description→Impact→Evidence→Remediation spine with justified, reproducible severity); when to use; pointer to `finding-template.md` and `severity-rating.md`; a Common Mistakes table built from the researched pitfalls (no impact articulation; scanner-dump vagueness; severity not justified; non-actionable remediation; non-reproducible PoC; instance-vs-class confusion; unredacted data; symptom-as-title). `**REQUIRED SUB-SKILL:** security-language`. **Final step:** "Before delivering, run `verify-security-language` on the finding."

- [ ] **Step 4: Application test**

Dispatch a subagent with the three files as context and raw facts ("SQLi in /api/login username param, confirmed via Burp, dumps users table"). Verify output: correct spine, names the vuln, justified severity with vector, reproducible redacted PoC, actionable remediation, CWE-89 reference, neutral language. Fix gaps in the skill if any.

- [ ] **Step 5: Commit**

```bash
git add skills/write-security-finding/
git commit -m "feat: add write-security-finding skill"
```

---

### Task 6: `write-security-incident-report` skill

**Files:**
- Create: `skills/write-security-incident-report/SKILL.md`
- Create: `skills/write-security-incident-report/incident-report-template.md`
- Create: `skills/write-security-incident-report/analysis-reference.md`

**Interfaces:**
- Consumes: `security-language` (Task 2), `verify-security-language` (Task 4).
- Produces: a NIST/PICERL-structured incident report structure + template.

- [ ] **Step 1: Write `analysis-reference.md`**

Reference for the hard parts:
- **Timeline:** chronological, UTC, ISO 8601 (`2026-06-28T14:32:07Z`), state "all times UTC" once. Columns: `Timestamp (UTC) | Event/Action | Source/Evidence | Actor`. Each entry evidence-anchored; mark inferred timing as estimated. Distinguish actor-activity vs. response timelines. Note dwell time, MTTD/MTTR.
- **IOC table:** grouped by type (SHA-256 preferred, IPs, domains, emails, paths, registry keys). Columns: `Type | Indicator | Context | Confidence | First/Last seen | Source`. **Defang** network IOCs (`hxxp://`, `192.168[.]1[.]1`). Mention STIX/TAXII, Sigma/YARA for appendices.
- **ATT&CK mapping:** table `Tactic | Technique ID | Technique Name | Observed behavior/evidence`; evidence-based, tie each to a timeline event.

- [ ] **Step 2: Write `incident-report-template.md`**

Skeleton with headed sections: `Metadata` (report ID, TLP classification, author, date, version, distribution, status draft/final), `Executive Summary` (non-technical), `Incident Overview/Classification` (type, severity, detection source, key dates), `Timeline` (UTC table), `Technical Detail / Root Cause`, `Impact & Scope` (systems: confirmed compromised vs. potentially exposed vs. cleared; data: *accessed* vs. *exfiltrated* vs. at-risk; business/regulatory), `Indicators of Compromise` (defanged table), `MITRE ATT&CK Mapping`, `Response Actions` (PICERL phases, who/what/when), `Lessons Learned` (blameless; what went well + improve; corrective actions with owner + due date + priority), `Appendices`.

- [ ] **Step 3: Write `SKILL.md`**

Frontmatter:
```yaml
---
name: write-security-incident-report
description: (hgto/security-skills) Use when writing a security incident report, post-incident report, security event report, or incident response writeup, or when documenting what happened during a security event with a timeline, scope, IOCs, and lessons learned.
---
```
Body: overview (NIST SP 800-61 / SANS PICERL spine; fact vs. assessment is paramount); when to use; pointers to template + `analysis-reference.md`; Common Mistakes table (speculation as fact; blame/naming people; missing/non-chronological/unlabeled-timezone timeline; "accessed" vs "exfiltrated" conflation; vague scope without stating visibility limits; recommendations with no owner/deadline; live un-defanged IOCs; ATT&CK unsupported by evidence; overstating certainty before forensics complete). `**REQUIRED SUB-SKILL:** security-language` (call out likelihood-vs-confidence + defanging). **Final step:** run `verify-security-language`.

- [ ] **Step 4: Application test**

Subagent with the three files + raw facts (phishing → macro → PowerShell → data accessed on one host, detected by EDR). Verify: UTC timeline, accessed-not-exfiltrated language, defanged IOCs, evidence-based ATT&CK (T1566.001, T1059.001), blameless lessons with owners, confidence qualifiers. Fix skill if gaps.

- [ ] **Step 5: Commit**

```bash
git add skills/write-security-incident-report/
git commit -m "feat: add write-security-incident-report skill"
```

---

### Task 7: `write-security-executive-summary` skill

**Files:**
- Create: `skills/write-security-executive-summary/SKILL.md`
- Create: `skills/write-security-executive-summary/exec-summary-template.md`
- Create: `skills/write-security-executive-summary/references-guide.md`

**Interfaces:**
- Consumes: `security-language` (Task 2), `verify-security-language` (Task 4).
- Produces: a BLUF-first executive summary structure + template + references guide.

- [ ] **Step 1: Write `references-guide.md`**

Authoritative source tiers (in credibility order): government/standards (NIST SP 800/1800, CISA advisories + KEV, NSA, FBI/IC3); frameworks (MITRE ATT&CK/D3FEND, CVE/CWE); vendor advisories (official bulletins — primary for patch/version); reputable reporting/research (corroboration, not primary basis). Annotated-reference format: **issuer + identifier + date + one-line "what it establishes and why relevant" + link to the primary source.** Example: "CISA Advisory AA23-320A, Nov 2023 — confirms active exploitation and affected versions; basis for our urgency. [link]". Rule: tie each major claim to a source.

- [ ] **Step 2: Write `exec-summary-template.md`**

Skeleton, descending priority, ~1 page: `BLUF` (≤3 sentences: situation + impact + the ask), `Context` (2–4 sentences), `Key Points` (3–5 bullets, point-first), `Risk / Business Impact` (quantified: $, downtime, records, % systems, compliance), `Recommendations / Decisions Needed` (prioritized; owner, cost, timeline, exact decision requested), `References` (annotated).

- [ ] **Step 3: Write `SKILL.md`**

Frontmatter:
```yaml
---
name: write-security-executive-summary
description: (hgto/security-skills) Use when writing an executive summary or leadership briefing on a security topic, vulnerability, threat, or incident for a non-technical or senior audience, or when asked for a BLUF, board summary, or bottom-line-up-front writeup.
---
```
Body: overview (BLUF = lead with conclusion + impact + ask; ~1 page; descending priority; business not technical language; calm, no FUD); when to use; pointers to template + `references-guide.md`; Common Mistakes table (too technical/jargon; burying the lede; no clear ask; fear-mongering/FUD; unsourced claims; unquantified risk; length bloat). `**REQUIRED SUB-SKILL:** security-language`. **Final step:** run `verify-security-language`.

- [ ] **Step 4: Application test**

Subagent with the three files + a topic (e.g. critical VPN CVE under active exploitation). Verify: BLUF leads with situation+impact+ask, quantified business risk, prioritized recommendation with owner/cost/timeline, annotated authoritative references (CISA/NIST/vendor with identifier+date), no FUD, neutral language. Fix skill if gaps.

- [ ] **Step 5: Commit**

```bash
git add skills/write-security-executive-summary/
git commit -m "feat: add write-security-executive-summary skill"
```

---

### Task 8: Finalize README, validate plugin, repo rename

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: all five completed skills.

- [ ] **Step 1: Finalize README**

Replace the placeholder skills list with the five finalized one-liners (matched to each skill's purpose), a short "How they work together" note (three doc skills require `security-language` and end by running `verify-security-language`), and an example invocation per skill. Remove the `<!-- finalized in Task 8 -->` marker.

- [ ] **Step 2: Validate all skill frontmatter**

Run a check that every `SKILL.md` has `name` (hyphen/letter/number only) and a `description` starting with `(hgto/security-skills) Use when`, and frontmatter ≤1024 chars:
```bash
for f in skills/*/SKILL.md; do
  echo "== $f"; head -5 "$f"
done
```
Expected: five files, each with valid frontmatter. Confirm no `@`-links: `! grep -rn '@skills/' skills/`.

- [ ] **Step 3: Full linter regression**

Run: `cd skills/verify-security-language && python3 -m pytest -v`
Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: finalize README for security-skills plugin"
```

- [ ] **Step 5: Rename the GitHub repo (requires user approval)**

This is an outward-facing action — confirm with the user, then:
```bash
gh repo rename security-skills --repo hgto/security-writing
git remote set-url origin git@github.com:hgto/security-skills.git
```
Then push the branch and open a PR (push requires explicit user approval per house rules).

---

## Self-Review

- **Spec coverage:** plugin scaffold (T1); central language standard with word table + estimative language (T2); verifier script (T3) + skill (T4); findings (T5); incident reports (T6); executive summaries (T7); README + validation + rename (T8). All five skills + the verifier script + rename covered.
- **Cross-references:** Tasks 4–7 each include `**REQUIRED SUB-SKILL:** security-language`; Tasks 5–7 each end by running `verify-security-language`. Consistent.
- **Type consistency:** `verify-language.py` interface (categories, `--json` shape, exit codes) defined in Task 3 and consumed unchanged in Task 4.
- **Naming:** all five final names used consistently in directory paths, frontmatter, and cross-references; every description begins with `(hgto/security-skills) `.
- **Testing:** discipline skills (T2, T4) have RED baseline + GREEN verify; document skills (T5–T7) have application tests; script (T3) has pytest TDD.
