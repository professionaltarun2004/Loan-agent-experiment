"""Baseline and experimental loan-agent policies."""

from .costs import expected_cost_proceed, expected_cost_request_evidence


def baseline_policy(posterior: dict, useful_evidence_available: bool) -> str:
    """Baseline for this experiment: always PROCEED."""
    return "PROCEED"


def policy_1_information_seeking(
    posteriors: dict, useful_evidence_available: bool
) -> str:
    """Preserved temporary information-seeking policy."""
    p_concerning = posteriors["concerning"]
    if p_concerning < 0.30:
        return "PROCEED"
    if useful_evidence_available:
        return "REQUEST_EVIDENCE"
    return "HUMAN_REVIEW"


def policy_2_cost_aware(
    posterior: dict,
    useful_evidence_available: bool,
    expected_request_cost=None,
    correct_proceed_cost: float = 0,
    wrong_proceed_cost: float = 100,
    human_review_cost: float = 30,
) -> str:
    """Select the lowest-cost action under the supplied synthetic costs."""
    costs = {
        "PROCEED": expected_cost_proceed(
            posterior, correct_proceed_cost, wrong_proceed_cost
        ),
        "HUMAN_REVIEW": human_review_cost,
    }
    if useful_evidence_available:
        if expected_request_cost is None:
            raise ValueError(
                "expected_request_cost is required when evidence is available"
            )
        costs["REQUEST_EVIDENCE"] = expected_request_cost
    return min(costs, key=costs.get)

