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

def action_policy(posteriors: dict, useful_evidence_available: bool) -> str:
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

    logger.debug("action_policy() called")
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

action = action_policy(posteriors, useful_evidence_available)

logger.debug("Inputs used  -> priors=%s, likelihoods=%s, evidence_available=%s",
             priors, likelihoods, useful_evidence_available)
logger.debug("request_cost = %s (SYNTHETIC experimental unit)", request_cost)
logger.info("Selected action: %s", action)
logger.info("request_cost introduced: %s experimental units (Stage 3 parameter)",
            request_cost)
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

print(f"\n[ LOG FILE ]")
print(f"  All runs are appended to: {LOG_FILE}")
print("=" * 55)
