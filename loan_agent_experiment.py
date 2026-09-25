"""Run the Week 1 synthetic loan-agent policy experiment."""

import logging
import os

from loan_agent.cases import CONTROLLED_CASES, MATRIX_CASES, SYNTHETIC_DISCLAIMER
from loan_agent.display import display_matrix_results, display_results
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
    display_matrix_results(matrix_results, MATRIX_CASES)

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
    logger.info("Experiment completed. Log saved to: %s", LOG_FILE)


if __name__ == "__main__":
    main()
