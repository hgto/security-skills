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
    assert r.returncode == 1
    assert "legal-term" in r.stdout

def test_flags_second_person_blame():
    r = run("You failed to apply the patch.")
    assert r.returncode == 1
    assert "second-person-blame" in r.stdout

def test_flags_compliance_opinion():
    r = run("This is a compliance violation of GDPR.")
    assert r.returncode == 1
    assert "legal-compliance-opinion" in r.stdout

def test_flags_violation_word():
    assert "legal-compliance-opinion" in run("This is a clear violation.").stdout

def test_flags_violates():
    assert "legal-compliance-opinion" in run("The system violates HIPAA.").stdout

def test_flags_vulnerability():
    r = run("We found a critical vulnerability in the login flow.")
    assert r.returncode == 1
    assert "weakness" in r.stdout

def test_flags_unauthorized_access():
    r = run("This allowed unauthorized access to records.")
    assert r.returncode == 1
    assert "inappropriate access" in r.stdout

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

def test_missing_file_exits_2():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "/nonexistent/path/that/does_not_exist.txt"],
        capture_output=True, text=True,
    )
    assert r.returncode == 2
    assert r.stderr  # a message should appear on stderr

# ---------------------------------------------------------------------------
# Proper-noun allow-list tests — official titles must not be flagged
# ---------------------------------------------------------------------------

def test_allows_cisa_kev():
    r = run("CISA's Known Exploited Vulnerabilities catalog lists it.")
    assert r.returncode == 0

def test_allows_nvd():
    r = run("See the NIST National Vulnerability Database for details.")
    assert r.returncode == 0

def test_allows_cve_fullname():
    r = run("Tracked as a Common Vulnerabilities and Exposures (CVE) entry.")
    assert r.returncode == 0

def test_bare_vulnerability_still_flagged():
    r = run("We discovered a vulnerability.")
    assert r.returncode == 1
    assert "weakness" in r.stdout

# ---------------------------------------------------------------------------
# URL suppression tests — banned slugs inside URLs must not be flagged
# ---------------------------------------------------------------------------

def test_allows_url_with_banned_slug():
    r = run("See https://www.cisa.gov/known-exploited-vulnerabilities-catalog for details.")
    assert r.returncode == 0

def test_url_does_not_suppress_surrounding_prose():
    r = run("This vulnerability is listed at https://example.com/known-exploited-vulnerabilities-catalog")
    assert r.returncode == 1
    assert "weakness" in r.stdout

def test_plain_url_clean():
    r = run("Patch per https://vendor.example.com/advisory/123")
    assert r.returncode == 0

# ---------------------------------------------------------------------------
# Cross-category multi-word precedence tests
# ---------------------------------------------------------------------------

def test_flags_in_breach_of():
    # "in breach of" (legal-compliance-opinion) must win over bare "breach"
    # (legal-term) even though legal-term appears earlier in CATEGORIES.
    r = run("They were in breach of HIPAA.")
    assert r.returncode == 1
    assert "legal-compliance-opinion" in r.stdout

def test_compliance_violation_still_specific():
    # Multi-word "compliance violation" must still win over bare "violation"
    # when the full phrase is present.
    r = run("This is a compliance violation.")
    assert "legal-compliance-opinion" in r.stdout
    assert "compliance violation" in r.stdout
