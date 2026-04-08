My trading bot made the following trades today: bought 150 shares of AAPL at $187.32, sold 80 at $191.15, bought 200 shares of MSFT at $412.88, sold all 200 at $409.22. Also, I had a covered call on AAPL (1 contract, strike $190, premium received $3.40) that expired worthless. Calculate my exact P&L for the day, broken down by position and total.

---
What it tests: Pure arithmetic accuracy, multi-step financial calculation, options math. This is a trap  - the math is straightforward but has multiple steps where errors compound.

---
Scoring:
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Arithmetic | 2+ errors | 1 error | All math correct |
| Breakdown Completeness | Missing positions | All positions but no separation | Full breakdown with realized vs. unrealized |
| Options Handling | Wrong or missing | Partially correct | Correct contract math (×100 shares) |

---
Category: ADVERSARIAL
Prompt: 9
