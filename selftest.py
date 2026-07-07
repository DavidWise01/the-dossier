#!/usr/bin/env python3
"""Verify-first self-test. Proves, with no network, that the dossier combines
findings honestly: (1) clean positives across independent membranes ADD bits to
a strong case; (2) a gated/contaminated finding contributes ZERO; (3) all-silence
stays near the prior; (4) a fired control invalidates the whole run; (5) the
verdict is always capped -- never the words proof/theft/proven; (6) more
independent clean crossings never lower the evidence (monotonic).
"""
from __future__ import annotations
from dossier import Finding, compile_dossier, posterior

fails = 0
def check(cond, msg):
    global fails
    print(("ok  · " if cond else "FAIL· ") + msg)
    fails += 0 if cond else 1

FO = "published"; SF = "weights"; HS = "context"


def pos(m, bits, note="clean hit"):
    return Finding(m, m, "positive", bits=bits, clean=True, note=note)

def silence(m, bits=-0.07):
    return Finding(m, m, "negative", bits=bits, clean=True, note="silence")

def gated(m, note="contaminated"):
    return Finding(m, m, "gated", bits=0.0, clean=False, note=note)

def control(m):
    return Finding(m, m, "control", bits=0.0, clean=True, note="held-out fired")


# 1. Three clean positives across independent membranes -> bits add -> strong case.
d = compile_dossier([pos(FO, 40), pos(SF, 60), pos(HS, 8)], prior=0.5)
check(abs(d["total_bits"] - 108) < 1e-9, f"independent membranes add bits (got {d['total_bits']})")
check(d["posterior"] > 0.999999, f"strong combined posterior (got {d['posterior']:.8f})")
check("MEMBERSHIP EVIDENCE" in d["verdict"] and "strong lead" in d["verdict"], "verdict names a strong lead")
check("3 independent membrane" in d["verdict"], "verdict counts the independent membranes")

# 2. A gated/contaminated finding contributes ZERO (not smuggled back in).
d2 = compile_dossier([pos(SF, 60), gated(HS, "public canary — could be quoting your copy")], prior=0.5)
check(abs(d2["total_bits"] - 60) < 1e-9, "gated finding contributes 0 bits")
check(len(d2["explained_away"]) == 1 and d2["n_positive_membranes"] == 1, "gated finding is listed as explained-away, not counted")

# 3. All-silence stays near the prior (silence across membranes is still silence).
d3 = compile_dossier([silence(FO), silence(SF), silence(HS)], prior=0.5)
check(abs(d3["posterior"] - 0.5) < 0.05, f"all-silence leaves posterior ~ prior (got {d3['posterior']:.3f})")
check("INSUFFICIENT" in d3["verdict"], "all-silence -> INSUFFICIENT, keep your mouth shut")

# 4. A fired control invalidates the whole run, however strong the rest looks.
d4 = compile_dossier([pos(FO, 40), pos(SF, 60), control(HS)], prior=0.5)
check(d4["invalid"] is True and "INVALID" in d4["verdict"], "a fired control -> INVALID")
check(d4["posterior"] is None, "invalid run reports no posterior")

# 5. The verdict is always capped: it never CLAIMS proof (no bare "proven"/"proof of X"),
#    and every membership-evidence verdict carries the explicit "NOT proof" disclaimer.
for dd in (d, d2, d3, d4):
    low = dd["verdict"].lower()
    check("proven" not in low, "verdict never says 'proven'")
    # the only time 'proof' may appear is inside the disclaimer 'not proof of ...'
    check(("proof" not in low) or ("not proof" in low), "'proof' appears only in the 'NOT proof' disclaimer")
for dd in (d, d2):  # the membership-evidence branch must disclaim explicitly
    check("not proof of theft" in dd["verdict"].lower(), "a positive verdict explicitly disclaims proof of theft")

# 6. Monotonic: adding another clean independent positive never lowers the evidence.
base = compile_dossier([pos(FO, 20)], prior=0.5)["total_bits"]
more = compile_dossier([pos(FO, 20), pos(SF, 20)], prior=0.5)["total_bits"]
check(more >= base, "more independent clean crossings never lower the evidence")

# 7. Sanity on the odds update.
check(abs(posterior(0.5, 0.0) - 0.5) < 1e-12, "0 bits updates nothing")

print("\n" + ("SOME CHECKS FAILED" if fails else "all dossier checks passed"))
raise SystemExit(1 if fails else 0)
