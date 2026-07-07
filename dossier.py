#!/usr/bin/env python3
"""the dossier — combine the boundary-crossing family's findings into ONE honest
case file, without overclaiming.

You have run the detectors. Each returns a FINDING on its membrane:
  - forward-observers : a published hit                (PUBLISHED membrane)
  - surfacing         : a certified surface / silence  (WEIGHTS membrane)
  - hearsay           : a corroborated lead / silence  (CONTEXT membrane)
The dossier folds these into a single belief that your marker was taken up,
and it does the folding the only defensible way:

  1. INDEPENDENT membranes carry INDEPENDENT evidence, so their Bayes factors
     multiply -- i.e. their BITS ADD. Three weak-but-clean crossings can add up
     to a strong case; one strong crossing already is one.
  2. A finding that was GATED by its own detector (contaminated / impossible /
     out-of-scope) contributes ZERO. It was explained away at the source; the
     dossier must not smuggle it back in.
  3. A NEGATIVE (silence) contributes its true, near-zero weight -- from the
     silence-gauge, a fraction of a bit under suppression -- never zero and
     never strong. Silence across membranes is still mostly silence.
  4. If a CONTROL fired anywhere (a held-out marker lit up), the whole run is
     INVALID. One fabricated finding poisons the case file.
  5. The verdict LANGUAGE is capped. However many bits accumulate, the dossier
     says "membership evidence / a strong lead across N membranes" -- never
     "proof," never "theft," never a causal or legal finding.
"""
from __future__ import annotations
import math
from dataclasses import dataclass

CLEAN_KINDS = ("positive", "negative")


def posterior(prior: float, bits: float) -> float:
    """Update a prior by a signed number of bits of evidence (odds form)."""
    if prior <= 0:
        return 0.0
    if prior >= 1:
        return 1.0
    if bits == math.inf:
        return 1.0
    if bits == -math.inf:
        return 0.0
    odds = prior / (1.0 - prior)
    post_odds = odds * (2.0 ** bits)
    if math.isinf(post_odds):
        return 1.0
    return post_odds / (1.0 + post_odds)


@dataclass
class Finding:
    membrane: str
    detector: str
    kind: str            # positive | negative | gated | control
    bits: float = 0.0    # signed evidence bits (positive supports membership)
    clean: bool = True   # False = gated/contaminated at the source
    note: str = ""


def _cap_verdict(n_pos, total_bits, post):
    if n_pos == 0:
        return ("INSUFFICIENT: no clean positive crossing; silence across membranes "
                "tells you little -- keep your mouth shut")
    strength = "a strong lead" if post > 0.99 else ("a lead" if post > 0.7 else "a weak lead")
    return (f"MEMBERSHIP EVIDENCE: {strength} across {n_pos} independent membrane(s), "
            f"{total_bits:.0f} bits total -- evidence, NOT proof of theft, causation, or a legal finding")


def compile_dossier(findings, prior: float = 0.5) -> dict:
    fired_controls = [f for f in findings if f.kind == "control"]
    if fired_controls:
        return {
            "verdict": "INVALID: a control fired -- a held-out marker lit up somewhere; "
                       "the whole case file is untrustworthy",
            "invalid": True,
            "posterior": None,
            "total_bits": None,
            "counted": [], "explained_away": [f.membrane for f in findings if not f.clean],
            "fired_controls": [f.membrane for f in fired_controls],
        }

    counted = [f for f in findings if f.clean and f.kind in CLEAN_KINDS]
    gated = [f for f in findings if not f.clean]
    total_bits = sum(f.bits for f in counted)
    n_pos = sum(1 for f in counted if f.kind == "positive" and f.bits > 0)
    post = posterior(prior, total_bits)

    return {
        "verdict": _cap_verdict(n_pos, total_bits, post),
        "invalid": False,
        "posterior": post,
        "total_bits": total_bits,
        "prior": prior,
        "n_positive_membranes": n_pos,
        "counted": [(f.membrane, f.kind, f.bits) for f in counted],
        "explained_away": [(f.membrane, f.note or "gated at source") for f in gated],
        "fired_controls": [],
    }


def report(d: dict) -> str:
    lines = ["# Dossier", "", d["verdict"], ""]
    if not d["invalid"]:
        lines += [f"prior            : {d['prior']}",
                  f"total evidence   : {d['total_bits']:.2f} bits",
                  f"posterior belief : {d['posterior']:.4f}",
                  f"clean crossings  : {len(d['counted'])}",
                  f"explained away   : {len(d['explained_away'])}"]
        for m, k, b in d["counted"]:
            lines.append(f"  + {m}: {k} ({b:+.1f} bits)")
        for m, why in d["explained_away"]:
            lines.append(f"  · {m}: not counted ({why})")
    return "\n".join(lines)
