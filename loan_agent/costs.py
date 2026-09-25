"""Synthetic experimental decision-cost calculations."""

from .bayesian import bayesian_update


def expected_cost_proceed(posterior: dict, correct_proceed_cost: float,
                          wrong_proceed_cost: float) -> float:
    return (
        posterior["legitimate"] * correct_proceed_cost
        + posterior["concerning"] * wrong_proceed_cost
    )


def downstream_expected_cost_after_evidence(posterior: dict, case: dict) -> float:
    """Probability-weighted least cost of PROCEED or HUMAN_REVIEW per outcome."""
    expected_downstream_cost = 0.0
    for outcome_name, probability in case["outcome_probabilities"].items():
        outcome_posterior = bayesian_update(
            posterior, case["outcome_likelihoods"][outcome_name]
        )
        proceed_cost = expected_cost_proceed(
            outcome_posterior,
            case["correct_proceed_cost"],
            case["wrong_proceed_cost"],
        )
        expected_downstream_cost += probability * min(
            proceed_cost, case["human_review_cost"]
        )
    return expected_downstream_cost


def expected_cost_request_evidence(posterior: dict, case: dict) -> float:
    """Request cost plus expected downstream cost across possible outcomes."""
    return case["request_cost"] + downstream_expected_cost_after_evidence(
        posterior, case
    )

