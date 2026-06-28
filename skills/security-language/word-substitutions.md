# Word Substitutions Reference

Columns: **Avoid** | **Use instead** | **Why** | **Legal term of art?**

This table is authoritative for all security writing produced under the `security-language` standard. When in doubt, choose the more precise, neutral alternative and state the observed fact rather than the conclusion.

---

## Substitution Table

| Avoid | Use instead | Why | Legal term? |
|---|---|---|---|
| attacker | external party, threat actor, the actor | presumes hostile intent + attribution | no |
| hacker | threat actor, external party | pejorative, imprecise | no |
| victim | affected party, impacted organization | frames legal posture; emotive | no |
| breach | incident, event, inappropriate access (state auth/authz + what was accessed) | regulatory term of art; triggers duties | YES — escalate to counsel |
| compromised (unconfirmed) | potentially affected, exposed to, accessed by | implies confirmed control | no |
| stolen / exfiltrated (unconfirmed) | accessed, transferred, copied, observed leaving | theft is a legal conclusion | YES — escalate to counsel |
| malicious | anomalous, unexpected, unsanctioned | intent claim, often unprovable | no |
| hacked | inappropriately accessed (detail what was accessed) | imprecise, sensational | no |
| vulnerability | weakness, potential weakness, finding, observed condition | infers a confirmed issue; compliance trigger | no (proper nouns CVE/CWE/CVSS kept) |
| unauthorized access | inappropriate access — state whether authentication occurred + whether the actor was authorized; detail what was accessed | ambiguous; conflates authN/authZ | no |
| negligent / careless / sloppy | did not align with [policy/standard], deviated from | blame + liability term | YES — escalate to counsel |
| obviously / clearly / of course | (delete; state the evidence) | asserts conclusion without support | no |
| catastrophic / devastating / massive | significant, material, [quantified] | hyperbole | no |
| destroyed / wiped | rendered unavailable, deleted, encrypted | be precise about observed effect | no |
| backdoor | undocumented access mechanism | loaded; presumes intent | no |
| weaponized | configured to exploit, used to deliver | militarized framing | no |
| guilty / culprit / perpetrator | responsible party, actor, source | criminal-law conclusion | no |
| spy / espionage (unconfirmed) | collection of information beyond approved scope | geopolitical conclusion | no |
| war / campaign (casual) | sustained activity, related set of events | reserve for evidenced usage | no |
| should have / failed to (personal) | (reframe to system/process) | personal blame; discoverable | no |
| violation / compliance violation / non-compliant | did not align with [control/policy]; gap relative to [control] | renders a compliance opinion we must not give | YES — flag for compliance/counsel |
| violates [regulation] / in breach of | may have implications under [framework]; recommend review by compliance/counsel | renders a legal/regulatory opinion | YES — flag for compliance/counsel |
| illegal / unlawful | (reframe to observed fact); flag for counsel | renders a legal conclusion | YES — flag for counsel |

---

## No Legal/Compliance Opinions

Never assert that an observed event constitutes a "violation," that a compliance or regulatory obligation has been breached, or that conduct was "illegal." These are conclusions that require legal or compliance expertise and may create discovery risk.

**Rule:** State the observed fact. Flag the matter explicitly for counsel or compliance to assess.

- Do not write: "This is a HIPAA violation."
- Write instead: "Protected health information was accessible without authentication; this may have implications under HIPAA — recommend review by compliance/counsel."

This principle extends every legal-term-of-art row in the table above (`breach`, `negligent`, `stolen / exfiltrated`, `violation`, `violates [regulation]`, `illegal / unlawful`). When those terms appear, the substitution is mandatory and a counsel/compliance flag is required.

---

## Absolutes Blocklist

Never use the following terms in security assessments or recommendations:

| Term | Replace with |
|---|---|
| unhackable | reduces the likelihood of … |
| 100% secure | no evidence of X was found |
| fully secure | mitigates … |
| fully eliminated | reduces the likelihood of … |
| completely eliminated | reduces the likelihood of … |
| guaranteed | no evidence of X was found; assessed with high confidence |
| impossible | no evidence of X was found; assessed with high confidence |
| cannot be breached | reduces the likelihood of … |

**Why:** Absolutes create contractual and legal exposure, are epistemically false in security, and undermine credibility if later refuted. Replace with probabilistic language (see `estimative-language.md`).
