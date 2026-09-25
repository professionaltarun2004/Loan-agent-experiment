# Week 1 Loan Agent Experiment

This is a small educational experiment about decisions under incomplete
information. It is a synthetic demonstration, not a lending or banking system.

## 1. Problem

**Implemented behavior:** The experiment represents an agent that observes
evidence, updates beliefs about a hidden state, and chooses among actions.

**Synthetic assumptions:** The case facts and numerical inputs are hand-selected
for the experiment.

## 2. Decision space

**Implemented behavior:** Available actions are `PROCEED`, `REQUEST_EVIDENCE`,
and `HUMAN_REVIEW`.

## 3. Partial observability

**Implemented behavior:** The agent receives evidence and a probability
distribution over hidden states; it does not receive the hidden state itself.

## 4. Hidden state

**Implemented behavior:** Cases use `legitimate` and `concerning` states.
Ground truth is stored separately and used only for evaluation.

**Limitation:** These labels are experimental abstractions, not real lending
categories.

## 5. Belief state

**Implemented behavior:** A belief state stores the agent's current probabilities
for `legitimate` and `concerning`.

## 6. Bayesian updating

**Implemented behavior:** `bayesian.py` computes normalized posterior beliefs
from priors and evidence likelihoods using Bayes' rule. Sequential evidence is
updated by passing each posterior forward as the next prior.

## 7. Active evidence gathering

**Implemented behavior:** When evidence is available, policies may choose
`REQUEST_EVIDENCE`. Its expected cost includes the request cost and the
probability-weighted downstream cost under each outcome model.

## 8. Human-in-the-loop

**Implemented behavior:** `HUMAN_REVIEW` is a defer/escalation action with a
synthetic cost. It is not counted as an incorrect state prediction.

## 9. Value/cost of information

**Implemented behavior:** Expected request cost is compared with the modeled
costs of proceeding and human review.

**Limitation:** This is a synthetic expected-cost calculation, not a validated
real-world value-of-information estimate.

## 10. Three policies

- **Baseline:** Always chooses `PROCEED`.
- **Policy 1:** Chooses `PROCEED` when P(concerning) is below 30%; otherwise it
  requests available evidence or selects human review when evidence is
  unavailable.
- **Policy 2:** Chooses the available action with the lowest modeled expected
  cost.

## 11. Synthetic experiment design

**Synthetic assumptions:** All priors, likelihoods, outcome probabilities,
hidden truths, and costs are invented experimental inputs. Costs are arbitrary
experimental units. No external or real banking data is used.

## 12. Five controlled cases

**Observed results:** The policies produced different actions across five
deliberately constructed cases. Their expected costs totaled 233.95 for
Baseline, 275.82 for Policy 1, and 153.25 for Policy 2. Baseline made two wrong
automated `PROCEED` decisions; Policy 1 and Policy 2 made none in this set.

**Limitation:** These figures describe only the five chosen cases.

## 13. 17-case matrix

**Implemented behavior:** The matrix varies belief, evidence availability and
informativeness, request cost, wrong-`PROCEED` cost, and human-review cost. It
includes a controlled Policy 1 threshold trio at approximately 29%, 30%, and
31% P(concerning), plus paired request-cost and review-cost cases.

## 14. Expanded evaluation

**Observed results (17 synthetic cases):**

| Metric | Baseline | Policy 1 | Policy 2 |
|---|---:|---:|---:|
| Total expected cost | 855.00 | 763.98 | 574.33 |
| Average expected cost | 50.29 | 44.94 | 33.78 |
| PROCEED count | 17 | 3 | 4 |
| REQUEST_EVIDENCE count | 0 | 11 | 6 |
| HUMAN_REVIEW count | 0 | 3 | 7 |
| Wrong automated PROCEED | 5 | 0 | 0 |
| Wrong PROCEED rate among PROCEED actions | 29.4% | 0.0% | 0.0% |

These metrics are descriptive and are not a policy ranking.

## 15. Deliberate failure tests

**Observed results:** Eight synthetic stress cases were run:

| Test | Observed behavior | Interpretation |
|---|---|---|
| Misleading evidence | High concerning posterior despite legitimate hidden truth; Baseline proceeds, both other policies review | Exposes likelihood misspecification sensitivity |
| Weak signal modeled as strong | Posterior shifts toward concern; Policy 1 and Policy 2 request evidence | Result follows the supplied, intentionally mismatched likelihood model |
| Conflicting sources | Sequential opposing signals return the belief to 50%; Policy 2 reviews | Depends on assumed likelihoods and source independence |
| Prohibitive evidence cost | Policy 1 requests; Policy 2 reviews | Shows Policy 1 does not weigh request cost; Policy 2 does |
| High wrong-PROCEED cost | Policy 1 proceeds; Policy 2 reviews | Policy 1's threshold does not account for consequence cost |
| Cheap, nearly useless evidence | Policy 1 requests; Policy 2 proceeds | Availability triggers Policy 1; Policy 2 weighs modeled information value and cost |
| High-confidence wrong prior | All policies proceed, incorrectly against hidden truth | Exposes reliance on supplied prior and likelihood calibration |
| Available but uninformative evidence | Policy 1 requests; Policy 2 reviews | Shows availability alone can trigger Policy 1 despite neutral outcomes |

## 16. Policy refinement

**Decision:** No policy changes were made. The observed failures either follow
Policy 1's stated design or arise from deliberately synthetic prior/likelihood
assumptions. The tests do not establish a code-level defect in Policy 2's cost
comparison.

## 17. Key observations

**Interpretation:** Baseline always proceeds. Policy 1 changes behavior at its
30% threshold and reacts to evidence availability, not its cost. Policy 2 can
change action when request or review costs change. At the threshold, Policy 1
proceeds just below 30% and does not proceed at 30% or 31%. In this matrix,
neither uncertainty nor evidence availability alone determines Policy 2's
choice.

## 18. Limitations

- The cases, probabilities, likelihoods, costs, and ground truths are synthetic.
- The threshold is an arbitrary experiment setting.
- Outcomes and likelihoods are manually specified; their calibration is not
  established.
- Sequential Bayesian updating relies on the supplied likelihood model and
  assumptions about how evidence sources relate.
- The evaluation uses a small, intentionally designed case set.

## 19. What this experiment does NOT prove

It does not prove real-world underwriting validity, safety, fairness, accuracy,
generalization, or that any policy is superior. The zero wrong-PROCEED counts
for two policies are limited to these synthetic cases and hidden truths.

## 20. Next possible experiment

Before expanding the case count, test calibrated likelihood assumptions and
prior sensitivity systematically. Preserve paired controls, document each
assumption, and compare observed policy behavior without treating this
synthetic exercise as lending guidance.
