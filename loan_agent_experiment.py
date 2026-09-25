"""Run the Week 1 synthetic loan-agent policy experiment."""

import logging
import os

from loan_agent.cases import (
    BREAK_CASES, CONTROLLED_CASES, MATRIX_CASES, SYNTHETIC_DISCLAIMER,
)
from loan_agent.display import display_break_results, display_matrix_results, display_results
from loan_agent.evaluation import (
    evaluate_cases,
    summarize_policy_performance,
    validate_stage9_matrix,
)


LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiment.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")],
)
logger = logging.getLogger("loan_agent")


def main() -> None:
    logger.info("Experiment started. %s", SYNTHETIC_DISCLAIMER)
    results = evaluate_cases(CONTROLLED_CASES)
    evaluation = summarize_policy_performance(results)
    display_results(results, evaluation)

    matrix_results = evaluate_cases(MATRIX_CASES)
    validate_stage9_matrix(results, MATRIX_CASES, matrix_results)
    matrix_summary = summarize_policy_performance(matrix_results)
    display_matrix_results(matrix_results, MATRIX_CASES, matrix_summary["policies"])

    break_results = evaluate_cases(BREAK_CASES)
    break_assessments = {
        "B01_MISLEADING_EVIDENCE": "Likelihood misspecification drives the result; model-assumption vulnerability, not a cost-comparison defect.",
        "B02_WEAK_SIGNAL_MISMODELED_STRONG": "Posterior and request value follow the supplied likelihoods; the weak-versus-strong mismatch is a synthetic modeling assumption.",
        "B03_CONFLICTING_SOURCES": "Opposing signals cancel under the supplied sequential likelihoods; independence/reliability assumptions limit interpretation.",
        "B04_PROHIBITIVE_EVIDENCE_COST": "Policy 1 still requests because it ignores cost by design; Policy 2 avoids the prohibitively costly request.",
        "B05_HIGH_WRONG_PROCEED_COST": "Policy 2 reviews because its modeled proceed cost exceeds review; Policy 1 retains its threshold-only behavior by design.",
        "B06_CHEAP_NEARLY_USELESS_EVIDENCE": "Policy 1 requests despite negligible value; Policy 2 proceeds because the request adds cost without changing downstream choices.",
        "B07_HIGH_CONFIDENCE_WRONG_PRIOR": "Automated proceed is wrong against hidden truth because supplied prior/likelihood beliefs remain misleading; this exposes model-calibration sensitivity.",
        "B08_EVIDENCE_AVAILABLE_NOT_USEFUL": "Policy 1 requests on availability; Policy 2 reviews because neutral evidence has no modeled value. This is the intended Policy 1 limitation.",
    }
    display_break_results(break_results, break_assessments)

    for result in results:
        logger.info(
            "%s | posterior=%s | actions=%s | expected_costs=%s",
            result["case_id"],
            {state: round(value, 6) for state, value in result["posterior"].items()},
            result["actions"],
            {policy: round(cost, 4)
             for policy, cost in result["expected_costs"].items()},
        )
    logger.info("Checkpoint C13: policy actions across %s controlled cases", len(results))
    for policy_name, summary in evaluation["policies"].items():
        logger.info(
            "%s evaluation | total_expected_cost=%.4f | average=%.4f | "
            "automated_proceed=%d | wrong_proceed=%d | wrong_rate=%.2f%% | wrong_cases=%s",
            policy_name, summary["total_expected_cost"],
            summary["average_expected_cost"], summary["automated_proceed_count"],
            summary["wrong_automated_proceed_count"],
            summary["wrong_proceed_rate"] * 100, summary["wrong_proceed_cases"],
        )
    logger.info("Checkpoint C14: controlled-case evaluation complete")
    logger.info("Stage 9 matrix: %d synthetic cases evaluated; threshold and paired-cost checks passed",
                len(matrix_results))
    for result in matrix_results:
        logger.info("%s | P(concerning)=%.6f | actions=%s | expected_costs=%s",
                    result["case_id"], result["posterior"]["concerning"],
                    result["actions"],
                    {policy: round(cost, 4)
                     for policy, cost in result["expected_costs"].items()})
    logger.info("C17 expanded matrix metrics: %s", matrix_summary)
    logger.info("C18 interpretation: policies respond differently to thresholds, evidence models, and costs; results are synthetic and designed.")
    for result in break_results:
        logger.info("C19 %s | stress=%s | posterior=%s | actions=%s | costs=%s | truth=%s (evaluation only) | assessment=%s",
                    result["case_id"], result["stress"], result["posterior"],
                    result["actions"], result["expected_costs"],
                    result["evaluation_only"]["hidden_ground_truth"],
                    break_assessments[result["case_id"]])
    logger.info("C20 policy review: no policy logic changes made.")
    logger.info("C21 final Week 1 report: README.md")
    logger.info("Experiment completed. Log saved to: %s", LOG_FILE)


if __name__ == "__main__":
    main()
