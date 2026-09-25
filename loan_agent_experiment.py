"""Run the Week 1 synthetic loan-agent policy experiment."""

import logging
import os

from loan_agent.cases import CONTROLLED_CASES, SYNTHETIC_DISCLAIMER
from loan_agent.display import display_results
from loan_agent.evaluation import evaluate_cases


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
    display_results(results)

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
    logger.info("Experiment completed. Log saved to: %s", LOG_FILE)


if __name__ == "__main__":
    main()
