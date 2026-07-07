# the-dossier — combine the family's findings without overclaiming

The capstone of the boundary-crossing family. You have run the detectors —
[forward-observers](https://davidwise01.github.io/forward-observers/) (published),
[surfacing](https://davidwise01.github.io/surfacing/) (weights),
[hearsay](https://davidwise01.github.io/hearsay/) (context). The dossier folds
their findings into **one** honest case file.

## The rules of honest combination

1. **Independent membranes add bits.** Different routes carry independent
   evidence, so their Bayes factors multiply — bits add. Three modest-but-clean
   crossings can make a strong case.
2. **Gated stays gated.** A finding a detector already explained away
   (contaminated / impossible) contributes **zero** — it can't be smuggled back in.
3. **Silence is near-mute.** A negative carries its true [silence-gauge](https://davidwise01.github.io/silence-gauge/)
   weight — a fraction of a bit under suppression — never zero, never strong.
4. **A fired control voids the file.** One held-out marker lighting up anywhere
   makes the whole run INVALID.
5. **The verdict is capped.** However many bits accumulate, it says *"a strong
   lead across N membranes — evidence, NOT proof of theft, causation, or a legal
   finding."* It never says proof. It never says proven.

## Verify first

```bash
python selftest.py
```

Proves with no network: independent membranes add bits to a strong case; a gated
finding contributes zero; all-silence stays near the prior (INSUFFICIENT); a fired
control invalidates the run; and the verdict never claims proof — every
membership verdict carries the explicit "NOT proof of theft" disclaimer.

## Files
- `dossier.py` — `compile_dossier` (fold findings, cap the verdict) + `posterior`
- `selftest.py` — the six honesty properties, no network
- `index.html` — compile a case file live; try to force a false "proven" (you can't)

---
David Lee Wise / ROOT0 / TriPod LLC · CC-BY-ND-4.0
