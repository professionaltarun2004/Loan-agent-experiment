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


def summarize_policy_performance(results: list[dict]) -> dict:
    """Aggregate expected costs and realized wrong automated PROCEED counts."""
    summary = {}
    for policy_name in ("Baseline", "Policy 1", "Policy 2"):
        total_expected_cost = sum(
            result["expected_costs"][policy_name] for result in results
        )
        automated_proceed_cases = [
            result for result in results
            if result["actions"][policy_name] == "PROCEED"
        ]
        wrong_proceed_cases = [
            result for result in automated_proceed_cases
            if result["evaluation_only"]["hidden_ground_truth"] != "legitimate"
        ]
        automated_count = len(automated_proceed_cases)
        wrong_count = len(wrong_proceed_cases)
        summary[policy_name] = {
            "total_expected_cost": total_expected_cost,
            "average_expected_cost": total_expected_cost / len(results) if results else 0,
            "automated_proceed_count": automated_count,
            "wrong_automated_proceed_count": wrong_count,
            "wrong_proceed_rate": wrong_count / automated_count if automated_count else 0,
            "wrong_proceed_cases": [result["case_id"] for result in wrong_proceed_cases],
        }

    # Add an explicit evaluation-only label for each case and policy action.
    case_evaluations = []
    for result in results:
        truth = result["evaluation_only"]["hidden_ground_truth"]
        policy_status = {}
        for policy_name, action in result["actions"].items():
            if action == "PROCEED":
                status = "CORRECT" if truth == "legitimate" else "WRONG"
                policy_status[policy_name] = f"PROCEED -> {status}"
            else:
                policy_status[policy_name] = f"{action} -> DEFER"
        case_evaluations.append({
            "case_id": result["case_id"],
            "hidden_ground_truth": truth,
            "policy_status": policy_status,
        })

    return {"policies": summary, "case_evaluations": case_evaluations}


def validate_stage9_matrix(controlled_results: list[dict], matrix_cases: list[dict],
                           matrix_results: list[dict]) -> None:
    """Assert the requested Stage 9 design checks without ranking policies."""
    assert len(controlled_results) == 5
    assert len(matrix_cases) == len(matrix_results) == 17
    assert [result["actions"] for result in controlled_results] == [
        {"Baseline": "PROCEED", "Policy 1": "REQUEST_EVIDENCE", "Policy 2": "HUMAN_REVIEW"},
        {"Baseline": "PROCEED", "Policy 1": "PROCEED", "Policy 2": "PROCEED"},
        {"Baseline": "PROCEED", "Policy 1": "REQUEST_EVIDENCE", "Policy 2": "REQUEST_EVIDENCE"},
        {"Baseline": "PROCEED", "Policy 1": "REQUEST_EVIDENCE", "Policy 2": "HUMAN_REVIEW"},
        {"Baseline": "PROCEED", "Policy 1": "REQUEST_EVIDENCE", "Policy 2": "PROCEED"},
    ]

    by_id = {result["case_id"]: result for result in matrix_results}
    for case_id, target in (
        ("M11_JUST_BELOW_POLICY_1_THRESHOLD", 0.29),
        ("M12_AT_POLICY_1_THRESHOLD", 0.30),
        ("M13_JUST_ABOVE_POLICY_1_THRESHOLD", 0.31),
    ):
        assert abs(by_id[case_id]["posterior"]["concerning"] - target) < 1e-6
    assert by_id["M11_JUST_BELOW_POLICY_1_THRESHOLD"]["actions"]["Policy 1"] == "PROCEED"
    assert by_id["M12_AT_POLICY_1_THRESHOLD"]["actions"]["Policy 1"] == "REQUEST_EVIDENCE"
    assert by_id["M13_JUST_ABOVE_POLICY_1_THRESHOLD"]["actions"]["Policy 1"] == "REQUEST_EVIDENCE"

    case_by_id = {case["case_id"]: case for case in matrix_cases}
    for first_id, second_id, changed_field in (
        ("M04_AMBIGUOUS_CHEAP_USEFUL_EVIDENCE", "M05_AMBIGUOUS_EXPENSIVE_EVIDENCE", "request_cost"),
        ("M15A_LOW_REVIEW_COST", "M15B_MODERATE_REVIEW_COST", "human_review_cost"),
        ("M15A_LOW_REVIEW_COST", "M15C_HIGH_REVIEW_COST", "human_review_cost"),
    ):
        first = {key: value for key, value in case_by_id[first_id].items()
                 if key not in ("case_id", changed_field)}
        second = {key: value for key, value in case_by_id[second_id].items()
                  if key not in ("case_id", changed_field)}
        assert first == second
