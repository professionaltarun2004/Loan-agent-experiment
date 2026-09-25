"""Run synthetic cases through Bayesian updating and the three policies."""

from .bayesian import bayesian_update
from .costs import expected_cost_proceed, expected_cost_request_evidence
from .policies import baseline_policy, policy_1_information_seeking, policy_2_cost_aware


def evaluate_case(case: dict) -> dict:
    """Return agent decisions/costs with evaluation-only truth kept separate."""
    posterior = bayesian_update(case["priors"], case["likelihoods"])
    available = case["useful_evidence_available"]
    request_cost = (
        expected_cost_request_evidence(posterior, case) if available else None
    )
    action_costs = {
        "PROCEED": expected_cost_proceed(
            posterior, case["correct_proceed_cost"], case["wrong_proceed_cost"]
        ),
        "HUMAN_REVIEW": case["human_review_cost"],
    }
    if request_cost is not None:
        action_costs["REQUEST_EVIDENCE"] = request_cost

    actions = {
        "Baseline": baseline_policy(posterior, available),
        "Policy 1": policy_1_information_seeking(posterior, available),
        "Policy 2": policy_2_cost_aware(
            posterior,
            available,
            expected_request_cost=request_cost,
            correct_proceed_cost=case["correct_proceed_cost"],
            wrong_proceed_cost=case["wrong_proceed_cost"],
            human_review_cost=case["human_review_cost"],
        ),
    }
    return {
        "case_id": case["case_id"],
        "observed_evidence": case["observed_evidence"],
        "posterior": posterior,
        "actions": actions,
        "expected_costs": {
            policy_name: action_costs[action]
            for policy_name, action in actions.items()
        },
        "expected_request_cost": request_cost,
        # Kept separate from the inputs passed into the policies.
        "evaluation_only": {"hidden_ground_truth": case["hidden_ground_truth"]},
    }


def evaluate_cases(cases: list[dict]) -> list[dict]:
    return [evaluate_case(case) for case in cases]

