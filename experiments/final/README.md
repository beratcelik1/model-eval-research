# Final Run Audit Trail

This directory contains the tracked April 8, 2026 final challenge-mode runs, the public score summary, representative conversation artifacts, and a recruiter-facing note on how observed failures translate into RL environment ideas.

## Canonical Raw Run Files

| Domain | Raw run file | UTC timestamp in file | SHA-256 |
|--------|--------------|-----------------------|---------|
| Investment Decisions | `investment-decisions_challenge_20260408_144955.json` | `2026-04-08T14:49:55+00:00` | `4abd154380c13262150afe6d02b77da07000184f15e4f11b08f7e5aa8e5e36b4` |
| Marketing Behavior | `marketing-behavior_challenge_20260408_145508.json` | `2026-04-08T14:55:08+00:00` | `0fb72209eaf3c0f389548637b3c0e69d06d3f7eaa9acd020105fb0a2b9500ad9` |
| Health Longevity | `health-longevity_challenge_20260408_150212.json` | `2026-04-08T15:02:12+00:00` | `5f7b3cbeff63106426db593cea64608c1bd505be6c2289650a9b36048a1579eb` |

## What Is Tracked Here

- Raw prompt-by-prompt responses for the final April 8 run
- Challenge prompts and second-round responses when a challenge was sent
- Public score summary in [final_grades.md](final_grades.md)
- Representative conversation excerpts in [conversation_artifacts.md](conversation_artifacts.md)
- Root-cause to RL-environment translation notes in [improvement_loop.md](improvement_loop.md)
- Prompt-level reconstruction notes in [rescoring_notes.md](rescoring_notes.md)

## Important Scoring Distinction

The raw JSONs contain a field called `phase1_score_pct`. That field is the inline checklist score used by `scripts/run_eval.py` to decide whether a challenge should be sent.

It is not the same thing as the published Phase 1 baseline shown in the report and [final_grades.md](final_grades.md). The published Phase 1 and challenge-review scores came from full-response review against the answer key, as documented in [report/main.tex](../../report/main.tex).

## What Is And Is Not Reproducible From Tracked Code

- Reproducible from tracked artifacts:
  - Raw model responses for the April 8 final run
  - Whether each prompt was challenged
  - The challenge text sent for challenged prompts
  - The inline checklist gate score used for challenge routing (`phase1_score_pct`)
  - File hashes and final-run provenance
- Not fully reproducible from tracked code alone:
  - The full set of prompt-level published Phase 1 review scores
  - The full set of prompt-level challenge-review scores used in the final public summary

Those published scores are preserved in the report and summary artifacts, but the repo does not currently contain a one-command regeneration script for every manual review value.

## Challenge Coverage In The Canonical Final Run

| Domain | Challenged prompts | Unchallenged prompts |
|--------|--------------------|----------------------|
| Investment Decisions | 8 / 10 | 2 / 10 |
| Marketing Behavior | 10 / 10 | 0 / 10 |
| Health Longevity | 4 / 10 | 6 / 10 |

These challenge counts are directly verifiable from the `challenge_sent` field in the raw run files and align with the challenge-status column in [final_grades.md](final_grades.md).

## How To Audit The Final Submission Quickly

1. Open the three raw run JSONs and inspect `metadata`, `prompt_text`, `phase1_response`, `challenge_text`, and `phase2_response`.
2. Compare challenge coverage against [final_grades.md](final_grades.md).
3. Check the worked scoring examples in [report/main.tex](../../report/main.tex).
4. Review [conversation_artifacts.md](conversation_artifacts.md) for representative prompt-level evidence.
5. Review [improvement_loop.md](improvement_loop.md) for how the observed failures would turn into training or environment work.
