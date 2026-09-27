# Employee safety screening — hybrid fix

The employee report screen now uses three layers:

1. The trained SIF model for the baseline score.
2. A deterministic safety ontology for explicit high-consequence mechanisms and dangerous precursors.
3. An optional Gemini semantic backstop only for ambiguous narratives that have no local rule match and an uncertain ML score.

The final value shown to employees is a **screening score**, not a calibrated probability. The raw ML score remains visible in the result note for transparency.

Examples covered by the local safety ontology include:

- actual falls from height
- electrocution / electrical shock
- caught-in / crushed / entangled machinery
- amputation
- vehicle / crane / suspended-load strikes
- explosion / flash fire
- confined-space emergencies
- pressure release / rupture
- burning smell, smoke and overheating precursors
- sparks / arcing / exposed or live wires
- gas / fuel / chemical odors and leaks
- missing critical controls / bypassed isolation / missing fall protection
- powered-tool injuries
- ordinary injuries that still need HSE review

Run the regression checks with:

```powershell
cd backend
python test_safety_screening.py
```
