"""Synthetic experiment cases. Ground truth is for evaluation only."""

SYNTHETIC_DISCLAIMER = (
    "All probabilities, likelihoods, and costs are synthetic experimental "
    "assumptions, not real banking statistics or financial values."
)

CURRENT_AMBIGUOUS_CASE = {
    "case_id": "CASE_1_CURRENT_AMBIGUOUS",
    "observed_evidence": "Declining balance for 3 months + unusual transaction pattern",
    "priors": {"legitimate": 0.50, "concerning": 0.50},
    "likelihoods": {"legitimate": 0.20, "concerning": 0.75},
    "useful_evidence_available": True,
    "request_cost": 10,
    "correct_proceed_cost": 0,
    "wrong_proceed_cost": 100,
    "human_review_cost": 30,
    "outcome_probabilities": {
        "SUPPORTING_LEGITIMATE": 0.20,
        "SUPPORTING_CONCERNING": 0.60,
        "UNCLEAR_CONFLICTING": 0.20,
    },
    "outcome_likelihoods": {
        "SUPPORTING_LEGITIMATE": {"legitimate": 0.60, "concerning": 0.80},
        "SUPPORTING_CONCERNING": {"legitimate": 0.20, "concerning": 0.80},
        "UNCLEAR_CONFLICTING": {"legitimate": 0.50, "concerning": 0.50},
    },
    "hidden_ground_truth": "concerning",
}

CONTROLLED_CASES = [
    CURRENT_AMBIGUOUS_CASE,
    {
        "case_id": "CASE_2_HIGH_CONFIDENCE_LEGITIMATE",
        "observed_evidence": "Synthetic evidence strongly consistent with the legitimate state",
        "priors": {"legitimate": 0.50, "concerning": 0.50},
        "likelihoods": {"legitimate": 0.95, "concerning": 0.05},
        "useful_evidence_available": False,
        "request_cost": 10,
        "correct_proceed_cost": 0,
        "wrong_proceed_cost": 100,
        "human_review_cost": 30,
        "outcome_probabilities": {"SUPPORTING_LEGITIMATE": 0.40, "SUPPORTING_CONCERNING": 0.40, "UNCLEAR_CONFLICTING": 0.20},
        "outcome_likelihoods": {
            "SUPPORTING_LEGITIMATE": {"legitimate": 0.90, "concerning": 0.10},
            "SUPPORTING_CONCERNING": {"legitimate": 0.10, "concerning": 0.90},
            "UNCLEAR_CONFLICTING": {"legitimate": 0.50, "concerning": 0.50},
        },
        "hidden_ground_truth": "legitimate",
    },
    {
        "case_id": "CASE_3_INFORMATION_WORTH_COLLECTING",
        "observed_evidence": "Synthetic initial evidence leaves substantial uncertainty",
        "priors": {"legitimate": 0.50, "concerning": 0.50},
        "likelihoods": {"legitimate": 0.50, "concerning": 0.50},
        "useful_evidence_available": True,
        "request_cost": 5,
        "correct_proceed_cost": 0,
        "wrong_proceed_cost": 100,
        "human_review_cost": 80,
        "outcome_probabilities": {"SUPPORTING_LEGITIMATE": 0.45, "SUPPORTING_CONCERNING": 0.45, "UNCLEAR_CONFLICTING": 0.10},
        "outcome_likelihoods": {
            "SUPPORTING_LEGITIMATE": {"legitimate": 0.95, "concerning": 0.05},
            "SUPPORTING_CONCERNING": {"legitimate": 0.05, "concerning": 0.95},
            "UNCLEAR_CONFLICTING": {"legitimate": 0.50, "concerning": 0.50},
        },
        "hidden_ground_truth": "legitimate",
    },
    {
        "case_id": "CASE_4_HUMAN_REVIEW_BEST",
        "observed_evidence": "Synthetic evidence leaves high concern and little expected resolution",
        "priors": {"legitimate": 0.50, "concerning": 0.50},
        "likelihoods": {"legitimate": 0.40, "concerning": 0.60},
        "useful_evidence_available": True,
        "request_cost": 100,
        "correct_proceed_cost": 0,
        "wrong_proceed_cost": 100,
        "human_review_cost": 30,
        "outcome_probabilities": {"SUPPORTING_LEGITIMATE": 0.20, "SUPPORTING_CONCERNING": 0.60, "UNCLEAR_CONFLICTING": 0.20},
        "outcome_likelihoods": {
            "SUPPORTING_LEGITIMATE": {"legitimate": 0.60, "concerning": 0.80},
            "SUPPORTING_CONCERNING": {"legitimate": 0.20, "concerning": 0.80},
            "UNCLEAR_CONFLICTING": {"legitimate": 0.50, "concerning": 0.50},
        },
        "hidden_ground_truth": "concerning",
    },
    {
        "case_id": "CASE_5_EVIDENCE_NOT_WORTH_COST",
        "observed_evidence": "Synthetic evidence modestly favors the legitimate state",
        "priors": {"legitimate": 0.50, "concerning": 0.50},
        "likelihoods": {"legitimate": 0.60, "concerning": 0.40},
        "useful_evidence_available": True,
        "request_cost": 20,
        "correct_proceed_cost": 0,
        "wrong_proceed_cost": 100,
        "human_review_cost": 45,
        "outcome_probabilities": {"SUPPORTING_LEGITIMATE": 0.30, "SUPPORTING_CONCERNING": 0.50, "UNCLEAR_CONFLICTING": 0.20},
        "outcome_likelihoods": {
            "SUPPORTING_LEGITIMATE": {"legitimate": 0.90, "concerning": 0.10},
            "SUPPORTING_CONCERNING": {"legitimate": 0.30, "concerning": 0.70},
            "UNCLEAR_CONFLICTING": {"legitimate": 0.50, "concerning": 0.50},
        },
        "hidden_ground_truth": "legitimate",
    },
]

