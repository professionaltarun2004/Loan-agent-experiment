"""
loan_agent_experiment.py
------------------------
Case 1 — Loan Document Agent: Bayesian Update + Action Policy Experiment
Research project: Assessing hidden financial states from observed loan behaviour.

OBSERVED EVIDENCE  : Declining balance for 3 months + unusual transaction pattern
HIDDEN STATES      : "legitimate" / "concerning"

DISCLAIMER: These are experimental abstractions, NOT validated lending categories.
The hidden-state labels and all likelihood values below are synthetic placeholders
chosen solely to demonstrate the mechanics of the Bayesian update.  They do not
represent established banking facts or real risk scores.
"""

import logging
import os

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
# Two handlers:
#   1. StreamHandler  — prints INFO+ messages to the console as usual
#   2. FileHandler    — writes DEBUG+ messages to experiment.log (persistent)
#
# This means every run appends a timestamped block to the log file,
# so you can track how inputs and outputs change across experiments.

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiment.log")

logging.basicConfig(
    level=logging.DEBUG,                        # capture everything at DEBUG and above
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),   # full detail -> file
        logging.StreamHandler(),                            # INFO+ -> console
    ],
)

logger = logging.getLogger("loan_agent")

logger.info("=" * 55)
logger.info("Experiment started: Case 1 - Loan Agent")
logger.info("=" * 55)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Define the Bayesian update function
# ─────────────────────────────────────────────────────────────────────────────

def bayesian_update(priors: dict, likelihoods: dict) -> dict:
    """
    Perform a single Bayesian update and return the posterior probabilities.

    Parameters
    ----------
    priors      : dict  — P(state)          before seeing the evidence
                          e.g. {"legitimate": 0.50, "concerning": 0.50}

    likelihoods : dict  — P(evidence|state) for each hidden state
                          e.g. {"legitimate": 0.20, "concerning": 0.75}

    Returns
    -------
    posteriors  : dict  — P(state|evidence) normalised so they sum to 1.0
    """

    logger.debug("bayesian_update() called")
    logger.debug("  Priors      : %s", priors)
    logger.debug("  Likelihoods : %s", likelihoods)

    # --- 2a. Multiply prior x likelihood for every state -------------------
    # This gives us the "joint probability" P(evidence n state)
    joint = {}
    for state in priors:
        joint[state] = priors[state] * likelihoods[state]

    logger.debug("  Joint probs : %s", {s: round(v, 6) for s, v in joint.items()})

    # --- 2b. Sum all joint probabilities to get the total evidence probability
    # P(evidence) = sum P(evidence|state) x P(state)  <- the normalising constant
    total_evidence = sum(joint.values())
    logger.debug("  P(evidence) normalising constant = %.6f", total_evidence)

    # --- 2c. Divide each joint probability by the total ----------------------
    # This is Bayes' theorem:  P(state|evidence) = P(evidence|state)xP(state) / P(evidence)
    posteriors = {}
    for state in joint:
        posteriors[state] = joint[state] / total_evidence

    logger.debug("  Posteriors  : %s", {s: round(v, 6) for s, v in posteriors.items()})
    logger.info("Bayesian update complete -> P(legitimate)=%.4f, P(concerning)=%.4f",
                posteriors["legitimate"], posteriors["concerning"])

    return posteriors


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Set up Case 1 inputs (SYNTHETIC values — clearly labelled)
# ─────────────────────────────────────────────────────────────────────────────

# Prior beliefs BEFORE seeing any evidence
# (equal split — we have no reason yet to favour one state)
priors = {
    "legitimate": 0.50,
    "concerning": 0.50,
}

# SYNTHETIC likelihoods — manually chosen for illustration purposes only.
# These are NOT from real data.  They are rough, unvalidated guesses used
# purely to exercise the Bayesian mechanics.  Do NOT treat these numbers as
# empirical facts about loan behaviour.
#
#   P(declining balance + unusual tx | legitimate) = 0.20
#     → Under a legitimate explanation this pattern seems relatively uncommon,
#       but we have no real evidence to support that number yet.
#
#   P(declining balance + unusual tx | concerning) = 0.75
#     → Under a concerning explanation this pattern seems more expected,
#       but again this is a placeholder — not a validated figure.
likelihoods = {
    "legitimate": 0.20,   # SYNTHETIC
    "concerning": 0.75,   # SYNTHETIC
}


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Define a temporary action-policy function
# ─────────────────────────────────────────────────────────────────────────────
# NOTE: This is a TEST POLICY — a temporary placeholder, not a final rule.
# It does NOT yet consider:
#   • the cost of requesting evidence
#   • the value of information (how much the new evidence would shift beliefs)
#   • any validated decision thresholds
# Those will be added in the next stage.

def policy_1_information_seeking(posteriors: dict, useful_evidence_available: bool) -> str:
    """
    A simple, temporary policy that maps a posterior + evidence availability
    to one of three actions.

    Actions
    -------
    PROCEED          — belief is already confident enough; no more evidence needed
    REQUEST_EVIDENCE — uncertainty is high enough AND extra evidence exists that
                       could meaningfully shift the posterior
    HUMAN_REVIEW     — belief is strongly concerning but no extra evidence exists,
                       so a human expert should decide

    Parameters
    ----------
    posteriors               : dict  — output of bayesian_update()
    useful_evidence_available: bool  — True if extra documents / statements exist

    NOTE: The words "confident enough" and "strongly concerning" are intentionally
    left as qualitative labels here.  Numerical thresholds will be derived from
    cost analysis in the next stage — we are not inventing them yet.
    """

    logger.debug("policy_1_information_seeking() called")
    logger.debug("  P(concerning)=%s  useful_evidence_available=%s",
                 round(posteriors["concerning"], 4), useful_evidence_available)

    # Grab the probability of the concerning state
    p_concerning = posteriors["concerning"]

    # Rule 1: If the concerning probability is LOW, we can proceed safely.
    # (Threshold is a temporary placeholder — not yet validated.)
    if p_concerning < 0.30:          # TODO: derive from cost analysis
        logger.info("Policy Rule 1 matched -> action: PROCEED  (P(concerning)=%.4f < 0.30)",
                    p_concerning)
        return "PROCEED"

    # Rule 2: Uncertainty is high enough that more evidence could help.
    # If extra evidence IS available, ask for it before deciding.
    if useful_evidence_available:
        logger.info("Policy Rule 2 matched -> action: REQUEST_EVIDENCE  "
                    "(P(concerning)=%.4f, evidence available)", p_concerning)
        return "REQUEST_EVIDENCE"

    # Rule 3: Concerning belief is high but no extra evidence exists.
    # Escalate to a human expert.
    logger.info("Policy Rule 3 matched -> action: HUMAN_REVIEW  "
                "(P(concerning)=%.4f, no evidence available)", p_concerning)
    return "HUMAN_REVIEW"


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 6A — GENERAL COST-AWARE POLICY
# ─────────────────────────────────────────────────────────────────────────────
def cost_aware_action_policy(
    posterior: dict,
    useful_evidence_available: bool,
    expected_request_cost=None,
) -> str:
    """Choose the available action with the lowest expected synthetic cost."""
    expected_proceed_cost = posterior["concerning"] * wrong_proceed_cost
    costs = {
        "PROCEED": expected_proceed_cost,
        "HUMAN_REVIEW": human_review_cost,
    }

    if useful_evidence_available:
        if expected_request_cost is None:
            raise ValueError(
                "expected_request_cost is required when useful evidence is available"
            )
        costs["REQUEST_EVIDENCE"] = expected_request_cost

    logger.info("Stage 6 - cost-aware policy action costs (SYNTHETIC)")
    logger.info("  Expected PROCEED cost = %.4f", expected_proceed_cost)
    if useful_evidence_available:
        logger.info("  Expected REQUEST_EVIDENCE cost = %.4f", expected_request_cost)
    else:
        logger.info("  REQUEST_EVIDENCE unavailable (no useful evidence)")
    logger.info("  HUMAN_REVIEW cost = %.4f", human_review_cost)

    selected_action = min(costs, key=costs.get)
    logger.info("  Selected cost-aware action = %s (cost %.4f)",
                selected_action, costs[selected_action])
    return selected_action


# Policy 2 name used for later policy comparisons.
policy_2_cost_aware = cost_aware_action_policy


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Run the Bayesian update, then apply the policy
# ─────────────────────────────────────────────────────────────────────────────

posteriors = bayesian_update(priors, likelihoods)

# For Case 1: previous 3-4 months of bank statements exist -> evidence is available
useful_evidence_available = True   # CASE-SPECIFIC input

# ── STAGE 3 PARAMETER ────────────────────────────────────────────────────────
# request_cost : synthetic experimental unit representing the cost of asking
# for the additional bank statements (e.g. analyst time, API call, delay).
# Value is deliberately arbitrary — chosen only to establish a cost scale.
# It is NOT derived from real banking data.  Will be compared against the
# Value of Information in the next stage to decide if requesting is worthwhile.
request_cost = 10   # SYNTHETIC — 10 experimental units

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5A — SYNTHETIC DECISION COST MODEL
# ─────────────────────────────────────────────────────────────────────────────
# All costs below are completely synthetic experimental units. They are NOT
# real banking costs, lending thresholds, or validated financial assumptions.
correct_proceed_cost = 0
wrong_proceed_cost = 100
human_review_cost = 30
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5C — POSSIBLE EVIDENCE OUTCOMES
# ─────────────────────────────────────────────────────────────────────────────
# These are synthetic experimental outcome categories, not real banking
# classifications. Outcome probabilities are intentionally not defined yet.
possible_evidence_outcomes = [
    {
        "name": "SUPPORTING_LEGITIMATE",
        "description": "The historical statements show a pattern that is more compatible with the legitimate state.",
        "probability": None,  # NOT DEFINED YET
    },
    {
        "name": "SUPPORTING_CONCERNING",
        "description": "The historical statements show a pattern that is more compatible with the concerning state.",
        "probability": None,  # NOT DEFINED YET
    },
    {
        "name": "UNCLEAR_CONFLICTING",
        "description": "The additional evidence is ambiguous, contradictory, incomplete, or otherwise does not meaningfully resolve the uncertainty.",
        "probability": None,  # NOT DEFINED YET
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5D — SYNTHETIC OUTCOME PROBABILITIES
# ─────────────────────────────────────────────────────────────────────────────
# These are synthetic experimental assumptions, NOT real banking statistics.
outcome_probabilities = {
    "SUPPORTING_LEGITIMATE": 0.20,  # SYNTHETIC
    "SUPPORTING_CONCERNING": 0.60,  # SYNTHETIC
    "UNCLEAR_CONFLICTING": 0.20,    # SYNTHETIC
}

outcome_probability_total = sum(outcome_probabilities.values())
if outcome_probability_total != 1.0:
    raise ValueError("Synthetic evidence outcome probabilities must sum to exactly 1.0")

logger.info("Stage 5D - synthetic outcome probabilities")
for outcome_name, probability in outcome_probabilities.items():
    logger.info("  %s = %.2f%% (SYNTHETIC)", outcome_name, probability * 100)
logger.info("  Total = %.2f%%", outcome_probability_total * 100)
logger.info("  These are synthetic assumptions for the experiment, not real banking statistics.")

logger.info("Stage 5C - possible evidence outcomes (synthetic categories)")
for index, outcome in enumerate(possible_evidence_outcomes, start=1):
    logger.info("  Outcome %s - %s", index, outcome["name"])
    logger.info("    Description: %s", outcome["description"])
    logger.info("    Outcome probability: %.2f%% (SYNTHETIC)",
                outcome_probabilities[outcome["name"]] * 100)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5B — EXPECTED COST OF ACTING NOW
# ─────────────────────────────────────────────────────────────────────────────
# Uses the posterior after the first evidence. All decision costs are synthetic
# experimental units; this does not change the action policy.
expected_cost_proceed_now = (
    posteriors["legitimate"] * correct_proceed_cost
    + posteriors["concerning"] * wrong_proceed_cost
)

logger.info("Stage 5B - expected cost of acting now (synthetic experimental units)")
logger.info("  P(legitimate) = %.6f; P(concerning) = %.6f",
            posteriors["legitimate"], posteriors["concerning"])
logger.info("  Cost if legitimate and PROCEED = %s; cost if concerning and PROCEED = %s",
            correct_proceed_cost, wrong_proceed_cost)
logger.info("  Expected cost of PROCEEDING NOW = %.4f", expected_cost_proceed_now)

action = policy_1_information_seeking(posteriors, useful_evidence_available)


# ─────────────────────────────────────────────────────────────────────────────
# STAGE 4 — Second Bayesian update after requesting evidence
# ─────────────────────────────────────────────────────────────────────────────
# This is one hypothetical synthetic outcome after requesting the statements.
# The likelihoods below are experimental placeholders only, not real banking
# statistics or validated risk values.
new_evidence = (
    "Previous 3-4 months show the same unusual transaction pattern consistently."
)

new_evidence_likelihoods = {
    "legitimate": 0.60,   # SYNTHETIC
    "concerning": 0.80,   # SYNTHETIC
}

# Sequential Bayesian update: the first posterior becomes the new prior.
new_priors = posteriors
second_posteriors = bayesian_update(new_priors, new_evidence_likelihoods)

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5F — COMPLETE SYNTHETIC OUTCOME LIKELIHOOD MODELS
# ─────────────────────────────────────────────────────────────────────────────
# Synthetic experimental assumptions only; these are NOT banking statistics.
outcome_likelihoods = {
    "SUPPORTING_LEGITIMATE": {
        "legitimate": 0.60, "concerning": 0.80,
    },
    "SUPPORTING_CONCERNING": {
        "legitimate": 0.20, "concerning": 0.80,
    },
    "UNCLEAR_CONFLICTING": {
        "legitimate": 0.50, "concerning": 0.50,
    },
}

scenario_posteriors = {
    outcome_name: bayesian_update(new_priors, likelihoods_for_outcome)
    for outcome_name, likelihoods_for_outcome in outcome_likelihoods.items()
}
for outcome_name, outcome_posterior in scenario_posteriors.items():
    if abs(sum(outcome_posterior.values()) - 1.0) > 1e-9:
        raise ValueError(f"Posterior for {outcome_name} does not sum to approximately 1.0")

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5G — CHOOSE THE BEST DOWNSTREAM ACTION AFTER EACH OUTCOME
# ─────────────────────────────────────────────────────────────────────────────
# Evaluate PROCEED and HUMAN_REVIEW only. Evidence gathering is complete.
downstream_decisions = {}
for outcome_name, outcome_posterior in scenario_posteriors.items():
    proceed_cost = outcome_posterior["concerning"] * wrong_proceed_cost
    review_cost = human_review_cost
    if proceed_cost < review_cost:
        selected_downstream_action = "PROCEED"
        selected_downstream_cost = proceed_cost
    else:
        selected_downstream_action = "HUMAN_REVIEW"
        selected_downstream_cost = review_cost

    downstream_decisions[outcome_name] = {
        "proceed_cost": proceed_cost,
        "human_review_cost": review_cost,
        "selected_action": selected_downstream_action,
        "selected_cost": selected_downstream_cost,
    }

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 5H — EXPECTED COST OF REQUESTING EVIDENCE
# ─────────────────────────────────────────────────────────────────────────────
# Cost-benefit values are experimental only, based entirely on synthetic inputs.
expected_cost_request_evidence = request_cost + sum(
    outcome_probabilities[outcome_name]
    * downstream_decisions[outcome_name]["selected_cost"]
    for outcome_name in outcome_probabilities
)
requesting_evidence_expected_benefit = (
    expected_cost_proceed_now - expected_cost_request_evidence
)

# Apply Policy 2 after all expected costs have been computed.
cost_aware_action = policy_2_cost_aware(
    posteriors,
    useful_evidence_available,
    expected_request_cost=expected_cost_request_evidence,
)

logger.info("Stage 4 - second Bayesian update after requesting evidence")
logger.info("Previous posterior / new prior: %s", new_priors)
logger.info("New evidence: %s", new_evidence)
logger.info("New evidence likelihoods (SYNTHETIC): %s", new_evidence_likelihoods)
logger.info("Second posterior: %s", second_posteriors)
logger.info("Updated P(legitimate | all evidence) = %.4f",
            second_posteriors["legitimate"])
logger.info("Updated P(concerning | all evidence) = %.4f",
            second_posteriors["concerning"])
logger.info("Stage 5F - outcome-to-posterior scenarios")
for outcome_name in outcome_probabilities:
    logger.info("  %s: outcome probability=%.2f%%, synthetic likelihoods=%s, posterior=%s",
                outcome_name, outcome_probabilities[outcome_name] * 100,
                outcome_likelihoods[outcome_name], scenario_posteriors[outcome_name])
logger.info("Stage 5G downstream actions (synthetic expected costs)")
for outcome_name, decision in downstream_decisions.items():
    logger.info("  %s: PROCEED cost=%.4f, HUMAN_REVIEW cost=%.4f, "
                "selected=%s at %.4f",
                outcome_name, decision["proceed_cost"],
                decision["human_review_cost"], decision["selected_action"],
                decision["selected_cost"])
logger.info("Stage 5H expected REQUEST_EVIDENCE cost = %.4f "
            "(synthetic experimental units)", expected_cost_request_evidence)
logger.info("Stage 5H expected benefit vs PROCEEDING NOW = %.4f "
            "(synthetic experimental units)", requesting_evidence_expected_benefit)
logger.info("Stage 6 cost-aware action selected = %s", cost_aware_action)

logger.debug("Inputs used  -> priors=%s, likelihoods=%s, evidence_available=%s",
             priors, likelihoods, useful_evidence_available)
logger.debug("request_cost = %s (SYNTHETIC experimental unit)", request_cost)
logger.info("Selected action: %s", action)
logger.info("request_cost introduced: %s experimental units (Stage 3 parameter)",
            request_cost)
logger.info("Stage 5A synthetic decision costs (experimental units): "
            "correct PROCEED=%s, wrong PROCEED=%s, REQUEST_EVIDENCE=%s, HUMAN_REVIEW=%s",
            correct_proceed_cost, wrong_proceed_cost, request_cost, human_review_cost)
logger.info("Expected cost of PROCEEDING NOW = %.4f synthetic experimental units",
            expected_cost_proceed_now)
logger.info("Experiment finished. Log saved to: %s", LOG_FILE)

print("=" * 55)
print("  CASE 1 - Loan Agent: Belief Update + Action Policy")
print("=" * 55)

print("\n[ OBSERVED EVIDENCE ]")
print("  Declining balance for 3 months + unusual transaction pattern")

print("\n[ PRIOR PROBABILITIES - P(state) ]")
for state, prob in priors.items():
    print(f"  P({state:<12}) = {prob:.2f}")

print("\n[ LIKELIHOODS - P(evidence | state)  *SYNTHETIC* ]")
for state, prob in likelihoods.items():
    print(f"  P(evidence | {state:<12}) = {prob:.2f}")

print("\n[ POSTERIOR PROBABILITIES - P(state | evidence) ]")
for state, prob in posteriors.items():
    print(f"  P({state:<12} | evidence) = {prob:.4f}  ({prob*100:.1f} %)")

print("\n[ ACTION POLICY  *TEMPORARY / TEST POLICY* ]")
print(f"  Useful additional evidence available : {useful_evidence_available}")
print(f"  Selected action                      : >>> {action} <<<")

print("\n[ REASONING ]")
print(f"  P(concerning) = {posteriors['concerning']:.1%} - above the PROCEED threshold.")
if useful_evidence_available:
    print("  Extra evidence (3-4 months of statements) exists -> agent asks for it")
    print("  before making a final decision.  No human escalation yet.")
else:
    print("  No extra evidence available -> escalate to human expert.")

print("\n[ COST OF REQUESTING EVIDENCE  *SYNTHETIC* ]")
print(f"  request_cost = {request_cost} experimental units")
print("  (Arbitrary scale — not a real banking figure.)")
print("  Action policy has NOT changed; cost is displayed only.")
print("  Next: compare this cost against Value of Information.")

print("\n" + "=" * 55)
print("CHECKPOINT 1 - INITIAL BELIEF")
print("=" * 55)
print(f"P(legitimate) = {priors['legitimate']:.4f}")
print(f"P(concerning) = {priors['concerning']:.4f}")

print("\n" + "=" * 55)
print("CHECKPOINT 2 - AFTER FIRST EVIDENCE")
print("=" * 55)
print("First posterior:")
print(f"  P(legitimate) = {posteriors['legitimate']:.4f}")
print(f"  P(concerning) = {posteriors['concerning']:.4f}")
print("Change from initial prior to first posterior:")
for state in priors:
    change = posteriors[state] - priors[state]
    print(f"  {state}: {change:+.4f} ({change * 100:+.2f} percentage points)")

print("\n" + "=" * 55)
print("CHECKPOINT 3 - FIRST ACTION")
print("=" * 55)
print(f"Selected action: {action}")
print("Reason: Additional evidence is available and the temporary policy requests it.")

print("\n" + "=" * 55)
print("CHECKPOINT 4 - AFTER REQUESTED EVIDENCE")
print("=" * 55)
print("Second posterior:")
print(f"  P(legitimate) = {second_posteriors['legitimate']:.4f}")
print(f"  P(concerning) = {second_posteriors['concerning']:.4f}")
print("Change from first posterior:")
for state in posteriors:
    change = second_posteriors[state] - posteriors[state]
    print(f"  {state}: {change:+.4f} ({change * 100:+.2f} percentage points)")

print("\n" + "=" * 55)
print("CHECKPOINT 5 - COST OF ACTING NOW")
print("=" * 55)
print(f"Expected cost of PROCEEDING NOW = {expected_cost_proceed_now:.4f} synthetic experimental units")

print("\n[ STAGE 5A - SYNTHETIC DECISION COST MODEL ]")
print(f"  Correct PROCEED cost       = {correct_proceed_cost}")
print(f"  Wrong PROCEED cost         = {wrong_proceed_cost}")
print(f"  REQUEST_EVIDENCE cost      = {request_cost}")
print(f"  HUMAN_REVIEW cost          = {human_review_cost}")
print("  All values are SYNTHETIC experimental units.")
print("  They are not real banking costs.")

print("\n" + "=" * 55)
print("STAGE 5C - POSSIBLE EVIDENCE OUTCOMES")
print("=" * 55)
for index, outcome in enumerate(possible_evidence_outcomes, start=1):
    print(f"\nOutcome {index} - {outcome['name']}")
    print(f"Description: {outcome['description']}")
    print(f"Probability: {outcome_probabilities[outcome['name']]:.0%} (SYNTHETIC)")

print("\n" + "=" * 55)
print("CHECKPOINT 6 - EVIDENCE OUTCOME SPACE")
print("=" * 55)
print(f"Possible outcomes = {len(possible_evidence_outcomes)}")
print("\n1. Supporting legitimate")
print("\n2. Supporting concerning")
print("\n3. Unclear/conflicting")

print("\n" + "=" * 55)
print("STAGE 5D - SYNTHETIC OUTCOME PROBABILITIES")
print("=" * 55)
for outcome_name, probability in outcome_probabilities.items():
    print(f"{outcome_name} = {probability * 100:.2f}%")
print(f"\nTotal = {outcome_probability_total * 100:.2f}%")

print("\n" + "=" * 55)
print("CHECKPOINT 7 - OUTCOME PROBABILITIES")
print("=" * 55)
print("Before requesting evidence, the experiment assumes:")
print("\n20% -> supporting legitimate")
print("60% -> supporting concerning")
print("20% -> unclear/conflicting")
print("\nThese are synthetic assumptions for the experiment.")

print("\n" + "=" * 55)
print("STAGE 5E - DECISION AFTER EACH EVIDENCE OUTCOME")
print("=" * 55)
print("Scenario posteriors use the synthetic likelihood models defined in Stage 5F.")

print("\n" + "=" * 55)
print("CHECKPOINT 8 - OUTCOME -> POSTERIOR")
print("=" * 55)
for outcome_name, outcome_posterior in scenario_posteriors.items():
    print(f"\n{outcome_name} (SYNTHETIC)")
    print(f"  Outcome probability = {outcome_probabilities[outcome_name]:.0%}")
    print(f"  P(outcome | legitimate) = {outcome_likelihoods[outcome_name]['legitimate']:.2f}")
    print(f"  P(outcome | concerning) = {outcome_likelihoods[outcome_name]['concerning']:.2f}")
    print(f"  P(legitimate) = {outcome_posterior['legitimate']:.4f}")
    print(f"  P(concerning) = {outcome_posterior['concerning']:.4f}")
    print(f"  Posterior total = {sum(outcome_posterior.values()):.4f}")

print("\n" + "=" * 55)
print("CHECKPOINT 9 - OUTCOME -> POSTERIOR (SYNTHETIC LIKELIHOOD MODELS)")
print("=" * 55)
print(f"{'Outcome':<26} {'Prob.':>8} {'Like L':>9} {'Like C':>9} {'Post L':>9} {'Post C':>9}")
for outcome_name, outcome_posterior in scenario_posteriors.items():
    print(f"{outcome_name:<26} {outcome_probabilities[outcome_name]:>7.0%} "
          f"{outcome_likelihoods[outcome_name]['legitimate']:>9.2f} "
          f"{outcome_likelihoods[outcome_name]['concerning']:>9.2f} "
          f"{outcome_posterior['legitimate']:>9.4f} "
          f"{outcome_posterior['concerning']:>9.4f}")
print("All likelihoods and outcome probabilities are SYNTHETIC experimental assumptions.")

print("\n" + "=" * 55)
print("STAGE 5G - DOWNSTREAM ACTION AFTER EACH OUTCOME")
print("=" * 55)
print("Synthetic costs; only PROCEED and HUMAN_REVIEW are evaluated here.")

print("\n" + "=" * 55)
print("CHECKPOINT 10 - BEST ACTION AFTER EACH OUTCOME")
print("=" * 55)
print(f"{'Outcome':<26} {'Posterior (L/C)':<25} {'PROCEED':>12} {'HUMAN_REVIEW':>14} {'Selected':>16}")
for outcome_name, outcome_posterior in scenario_posteriors.items():
    decision = downstream_decisions[outcome_name]
    posterior_label = (f"{outcome_posterior['legitimate']:.4f}/"
                       f"{outcome_posterior['concerning']:.4f}")
    print(f"{outcome_name:<26} {posterior_label:<25} "
          f"{decision['proceed_cost']:>12.4f} "
          f"{decision['human_review_cost']:>14.2f} "
          f"{decision['selected_action']:>16}")

print("\n" + "=" * 55)
print("STAGE 5H - EXPECTED COST OF REQUESTING EVIDENCE")
print("=" * 55)
for outcome_name in outcome_probabilities:
    decision = downstream_decisions[outcome_name]
    weighted_cost = outcome_probabilities[outcome_name] * decision["selected_cost"]
    print(f"{outcome_name}: {outcome_probabilities[outcome_name]:.0%} x "
          f"{decision['selected_cost']:.4f} = {weighted_cost:.4f}")
print(f"Request cost = {request_cost:.4f} synthetic experimental units")
print(f"Expected cost of REQUESTING EVIDENCE = {expected_cost_request_evidence:.4f} "
      "synthetic experimental units")
print(f"Expected cost of PROCEEDING NOW = {expected_cost_proceed_now:.4f} "
      "synthetic experimental units")
print(f"Expected benefit of requesting evidence = {requesting_evidence_expected_benefit:.4f} "
      "synthetic experimental units")
if expected_cost_request_evidence < expected_cost_proceed_now:
    print("Under the CURRENT SYNTHETIC COST MODEL, requesting evidence has the lower expected cost.")
elif expected_cost_request_evidence > expected_cost_proceed_now:
    print("Under the CURRENT SYNTHETIC COST MODEL, proceeding now has the lower expected cost.")
else:
    print("Under the CURRENT SYNTHETIC COST MODEL, both choices have equal expected cost.")
print("This is an experimental cost-benefit calculation, not a real-world banking estimate.")

print("\n" + "=" * 55)
print("STAGE 6 - COST-AWARE ACTION POLICY")
print("=" * 55)
print("Stage 6A: policy_2_cost_aware() compares expected costs of available actions.")

print("\n" + "=" * 55)
print("CHECKPOINT 12 - COST-AWARE POLICY")
print("=" * 55)
print(f"Current posterior: legitimate={posteriors['legitimate']:.4f}, "
      f"concerning={posteriors['concerning']:.4f}")
print(f"Expected PROCEED cost = {posteriors['concerning'] * wrong_proceed_cost:.4f}")
print(f"Expected REQUEST_EVIDENCE cost = {expected_cost_request_evidence:.4f}")
print(f"HUMAN_REVIEW cost = {human_review_cost:.4f}")
print(f"Selected action = {cost_aware_action}")
print("Reason: HUMAN_REVIEW has the lowest expected cost under the current synthetic cost model.")

print("\n" + "=" * 55)
print("STAGE 6C - POLICY INTERPRETATION")
print("=" * 55)
print("The agent is no longer deciding from probability alone.")
print("It compares the expected cost of available actions.")
print("REQUEST_EVIDENCE is useful only when its expected downstream benefit")
print("justifies its cost.")
print("All values and assumptions are SYNTHETIC; they do not represent real lending.")

print("\n[ STAGE 5B - EXPECTED COST OF ACTING NOW ]")
print(f"  P(legitimate) = {posteriors['legitimate']:.6f}")
print(f"  P(concerning) = {posteriors['concerning']:.6f}")
print(f"\n  Cost if legitimate and PROCEED = {correct_proceed_cost}")
print(f"  Cost if concerning and PROCEED = {wrong_proceed_cost}")
print(f"\n  Expected cost of PROCEEDING NOW = {expected_cost_proceed_now:.4f} synthetic experimental units")
print("  This is the expected cost of stopping now and proceeding without requesting more evidence.")

print("\n[ STAGE 4 - NEW EVIDENCE ]")
print("  New evidence:")
print(f"  {new_evidence}")

print("\n[ SECOND BAYESIAN UPDATE ]")
print(f"  New prior P(legitimate) = {new_priors['legitimate']:.4f}")
print(f"  New prior P(concerning) = {new_priors['concerning']:.4f}")
print("\n  New evidence likelihoods  *SYNTHETIC*")
print(f"  P(new evidence | legitimate) = {new_evidence_likelihoods['legitimate']:.2f}  *SYNTHETIC*")
print(f"  P(new evidence | concerning) = {new_evidence_likelihoods['concerning']:.2f}  *SYNTHETIC*")
print(f"\n  Updated P(legitimate | all evidence) = {second_posteriors['legitimate']:.4f}")
print(f"  Updated P(concerning | all evidence) = {second_posteriors['concerning']:.4f}")

print("\nStage 4 complete.")
print("The second Bayesian update is now implemented.")
print("The Stage 4 update is retained as the SUPPORTING_LEGITIMATE scenario model.")
print("\nStage 5A complete.")
print("Decision costs are now defined.")
print("Next: calculate the expected cost of acting now versus requesting information.")
print("\nStage 5B complete.")
print("Expected cost of acting now has been calculated.")
print("Next: calculate the expected cost after requesting information.")
print("\nStage 5C complete.")
print("Three possible evidence outcomes are now explicitly represented.")
print("Next: assign synthetic outcome probabilities and calculate the expected cost after requesting evidence.")
print("\nStage 5D complete.")
print("Outcome probabilities are now defined.")
print("Next: calculate the decision cost associated with each outcome.")
print("\nStage 5E complete.")
print("Outcome probabilities and posterior calculations are now explicitly separated.")
print("The outcome likelihood models and downstream comparisons are completed below.")

print("\nStages 5F-5H complete. Next stage: convert this cost calculation into the cost-aware action policy.")

print("\n" + "=" * 55)
print("EXPERIMENT CHECKPOINT SUMMARY")
print("=" * 55)
print(f"C1 Initial belief: legitimate={priors['legitimate']:.4f}, concerning={priors['concerning']:.4f}")
print(f"C2 First posterior: legitimate={posteriors['legitimate']:.4f}, concerning={posteriors['concerning']:.4f}")
print(f"C3 Action: {action}")
print(f"C4 Second posterior: legitimate={second_posteriors['legitimate']:.4f}, concerning={second_posteriors['concerning']:.4f}")
print(f"C5 Expected cost of proceeding now: {expected_cost_proceed_now:.4f} synthetic experimental units")
print("C6 Evidence outcome space: SUPPORTING_LEGITIMATE, SUPPORTING_CONCERNING, UNCLEAR_CONFLICTING")
print("C7 Outcome probabilities: 20%, 60%, 20% (SYNTHETIC)")
print("C8 Outcome -> posterior:")
for outcome_name, outcome_posterior in scenario_posteriors.items():
    print(f"   {outcome_name}: legitimate={outcome_posterior['legitimate']:.4f}, "
          f"concerning={outcome_posterior['concerning']:.4f}")
print("C9 Completed outcome likelihood models: all three (SYNTHETIC)")
print("C10 Best downstream action after each outcome:")
for outcome_name, decision in downstream_decisions.items():
    print(f"   {outcome_name}: {decision['selected_action']}")
print(f"C11 Expected cost of requesting evidence: {expected_cost_request_evidence:.4f} "
      "synthetic experimental units")
print(f"C12 Cost-aware policy: {cost_aware_action}")

print(f"\n[ LOG FILE ]")
print(f"  All runs are appended to: {LOG_FILE}")
print("=" * 55)
print("\nStage 6 complete.")
print("The agent now has a cost-aware decision policy.")
print("\nNext stage:")
print("construct controlled cases that can expose differences between")
print("the baseline, information-seeking policy, and cost-aware policy.")
