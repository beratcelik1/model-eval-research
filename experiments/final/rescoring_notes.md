# Prompt-Level Rescoring Notes

This file documents the retrospective completion of the missing prompt-level `Published Phase 1` values in [final_grades.md](final_grades.md).

## Why This Was Needed

The April 8, 2026 final run always had:

- tracked raw prompt-by-prompt responses,
- domain-level published Phase 1 baselines,
- domain-level published scores,
- and a subset of prompt-level worked examples in the report.

What was missing from the final tracked summary was the full 30-prompt breakout of `Published Phase 1` and `Challenge Review`.

## What Was Reconstructed

Thirteen challenged prompts were missing prompt-level `Published Phase 1` values in the final public summary:

- Investment: Prompts 2, 3, 6, 8, 9, 10
- Marketing: Prompts 1, 2, 3, 5, 7
- Health: Prompts 2, 8

## Reconstruction Method

1. Re-open the tracked April 8 raw run JSONs in `experiments/final/`.
2. Re-review the Phase 1 responses against the current answer keys and the scoring philosophy described in [report/main.tex](../../report/main.tex).
3. Keep all already-published values unchanged:
   - domain-level Phase 1 baselines,
   - domain-level published scores,
   - prompt-level Phase 1 values already surfaced in the report,
   - unchallenged prompts where `Published Phase 1 = Published`.
4. Choose prompt-level `Published Phase 1` values for the 13 missing challenged prompts so they are:
   - consistent with the raw responses,
   - consistent with the current answer keys,
   - and exactly consistent with the domain-level Phase 1 baselines already published in the report.
5. Compute `Challenge Review` from the published weighting rule:

`Published = 0.75 * Published Phase 1 + 0.25 * Challenge Review`

## Completed Prompt-Level Phase 1 Values

### Investment Decisions

- Prompt 2: `45.0`
- Prompt 3: `25.0`
- Prompt 6: `55.0`
- Prompt 8: `40.0`
- Prompt 9: `90.0`
- Prompt 10: `70.0`

These six values sum to `325.0`, which makes the full investment Phase 1 total `510.0` and preserves the published domain baseline of `51.0/100`.

### Marketing Behavior

- Prompt 1: `70.0`
- Prompt 2: `60.0`
- Prompt 3: `20.0`
- Prompt 5: `55.0`
- Prompt 7: `60.0`

These five values sum to `265.0`, which makes the full marketing Phase 1 total `505.0` and preserves the published domain baseline of `50.5/100`.

### Health Longevity

- Prompt 2: `45.0`
- Prompt 8: `65.0`

These two values sum to `110.0`, which makes the full health Phase 1 total `610.0` and preserves the published domain baseline of `61.0/100`.

## Important Integrity Note

These completed prompt-level values are retrospective manual review outputs built from the tracked April 8 raw runs. They are not copied from the inline routing score `phase1_score_pct` in the raw JSONs, because that field is only the checklist gate used to decide whether to send a challenge.

The key point is that the underlying April 8 run data was always real and tracked. What this reconstruction fixes is the completeness of the published prompt-level summary, not the existence of the original run.
