# BER Cost Planner — V2 Wish List

Items noted during V1 development for future consideration.

---

## Works Selector — Refurbishment

### Roof Alterations section
The current works selector shows generic roof strip-out and fit-out items. For V2, replace/supplement with a dedicated **Roof Alterations** section covering specific scope items as standalone checkboxes with their own allowance rates:

- Vaulted / cathedral ceiling conversion
- Loft conversion (habitable)
- Dormer addition
- Warm roof upgrade (cold roof converted to warm roof build-up)
- Structural ridge beam / load-bearing alteration
- Flat roof replacement (full system — insulation, membrane, upstands)

Rationale: roof works in a refurb are rarely a standard menu — filtering by roof type (pitched/flat) would still miss edge cases. Better to let the assessor pick specific interventions explicitly.

---

## Energy Upgrade — BER-Driven Scope Validation

### Current/Target BER gap → flag whether selected measures are sufficient
Currently the Current BER and Target BER fields are report context only (they appear in the report header and are passed to the AI prompt). For V2, use the gap between current and target to:

- Estimate the BER improvement each selected measure is likely to deliver (kWh/m²/yr reduction using DEAP lookup tables)
- Sum the estimated improvement across all ticked measures
- Flag if the total estimated improvement falls short of bridging the gap to the target rating
- Show a "likely BER outcome" indicator in the works selector (e.g. "estimated outcome: C — target is B, add further measures")

Rationale: a QS preparing a preliminary cost plan needs to know whether the scope they've priced is actually sufficient to hit the BER target the client needs (e.g. B2 for mortgage drawdown, A for SEAI grant top-up eligibility). This turns the tool from a cost estimator into a scope-adequacy checker as well.

---
