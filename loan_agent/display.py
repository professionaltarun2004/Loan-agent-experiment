"""Concise terminal presentation for the experiment results."""


RULE = "-" * 55


def display_results(results: list[dict], evaluation: dict) -> None:
    print(RULE)
    print("WEEK 1 - LOAN AGENT EXPERIMENT")
    print(RULE)

    reference = results[0]
    print("\nREFERENCE CASE\n")
    print(f"Case:\n{reference['case_id']}")
    print("\nInitial posterior:")
    print(f"Legitimate: {reference['posterior']['legitimate']:.2%}")
    print(f"Concerning: {reference['posterior']['concerning']:.2%}")
    print("\nActions:")
    for policy_name in ("Baseline", "Policy 1", "Policy 2"):
        print(f"{policy_name:<17} -> {reference['actions'][policy_name]}")
    print("\nExpected costs (synthetic experimental units):")
    for policy_name in ("Baseline", "Policy 1", "Policy 2"):
        print(f"{policy_name:<17} -> {reference['expected_costs'][policy_name]:.2f}")

    print(f"\n{RULE}\nCONTROLLED CASES\n{RULE}\n")
    print(f"{'Case':<42} {'Baseline':<15} {'Policy 1':<19} {'Policy 2'}")
    for result in results:
        actions = result["actions"]
        print(f"{result['case_id']:<42} {actions['Baseline']:<15} "
              f"{actions['Policy 1']:<19} {actions['Policy 2']}")

    print(f"\n{RULE}\nCHECKPOINT\n{RULE}")
    print("C13 - Policy actions across controlled cases")

    print(f"\n{RULE}\nSTAGE 8 - POLICY EVALUATION\n{RULE}")
    print(f"{'Metric':<34} {'Baseline':>12} {'Policy 1':>12} {'Policy 2':>12}")
    metrics = (
        ("Total expected cost", "total_expected_cost", ".2f"),
        ("Average expected cost", "average_expected_cost", ".2f"),
        ("Automated PROCEED count", "automated_proceed_count", "d"),
        ("Wrong automated PROCEED", "wrong_automated_proceed_count", "d"),
        ("Wrong PROCEED rate", "wrong_proceed_rate", ".1%"),
    )
    policy_summary = evaluation["policies"]
    for label, key, format_spec in metrics:
        values = [format(policy_summary[name][key], format_spec)
                  for name in ("Baseline", "Policy 1", "Policy 2")]
        print(f"{label:<34} {values[0]:>12} {values[1]:>12} {values[2]:>12}")

    print(f"\n{RULE}\nCASE-LEVEL EVALUATION\n{RULE}")
    print(f"{'Case':<42} {'Ground Truth':<15} {'Baseline':<26} "
          f"{'Policy 1':<26} {'Policy 2'}")
    for case_result in evaluation["case_evaluations"]:
        statuses = case_result["policy_status"]
        print(f"{case_result['case_id']:<42} "
              f"{case_result['hidden_ground_truth']:<15} "
              f"{statuses['Baseline']:<26} {statuses['Policy 1']:<26} "
              f"{statuses['Policy 2']}")

    print("\nWrong automated PROCEED cases:")
    for policy_name in ("Baseline", "Policy 1", "Policy 2"):
        wrong_cases = policy_summary[policy_name]["wrong_proceed_cases"]
        label = ", ".join(wrong_cases) if wrong_cases else "None"
        print(f"  {policy_name}: {label}")

    print(f"\n{RULE}\nCHECKPOINT\n{RULE}")
    print("C14 - Controlled-case policy evaluation complete")


def display_matrix_results(results: list[dict], cases: list[dict], summary: dict) -> None:
    by_id = {result["case_id"]: result for result in results}
    case_by_id = {case["case_id"]: case for case in cases}
    print(f"\n{RULE}\nSTAGE 9 - SYNTHETIC MATRIX\n{RULE}")
    print("All matrix values are synthetic experimental assumptions.")
    print(f"\n{'Case':<42} {'P(concerning)':>14} {'Baseline':<16} "
          f"{'Policy 1':<19} {'Policy 2'}")
    for result in results:
        actions = result["actions"]
        print(f"{result['case_id']:<42} "
              f"{result['posterior']['concerning']:>13.2%} "
              f"{actions['Baseline']:<16} {actions['Policy 1']:<19} "
              f"{actions['Policy 2']}")

    print("\nExpanded 17-case metrics (expected-cost units are synthetic):")
    print(f"{'Metric':<33} {'Baseline':>10} {'Policy 1':>10} {'Policy 2':>10}")
    matrix_metrics = (
        ("Total expected cost", "total_expected_cost", ".2f"),
        ("Average expected cost", "average_expected_cost", ".2f"),
        ("PROCEED count", "proceed_count", "d"),
        ("REQUEST_EVIDENCE count", "request_evidence_count", "d"),
        ("HUMAN_REVIEW count", "human_review_count", "d"),
        ("Automated PROCEED count", "automated_proceed_count", "d"),
        ("Wrong automated PROCEED", "wrong_automated_proceed_count", "d"),
        ("Wrong PROCEED rate", "wrong_proceed_rate", ".1%"),
    )
    for label, key, format_spec in matrix_metrics:
        values = [format(summary[name][key], format_spec)
                  for name in ("Baseline", "Policy 1", "Policy 2")]
        print(f"{label:<33} {values[0]:>10} {values[1]:>10} {values[2]:>10}")
    print("C17 - Expanded 17-case evaluation complete")

    print(f"\n{RULE}\nTHRESHOLD TEST\n{RULE}")
    for case_id in (
        "M11_JUST_BELOW_POLICY_1_THRESHOLD",
        "M12_AT_POLICY_1_THRESHOLD",
        "M13_JUST_ABOVE_POLICY_1_THRESHOLD",
    ):
        result = by_id[case_id]
        print(f"{case_id}: P(concerning)="
              f"{result['posterior']['concerning']:.6f}; "
              f"Policy 1={result['actions']['Policy 1']}")

    print(f"\n{RULE}\nCOST SENSITIVITY\n{RULE}")
    for case_id in (
        "M04_AMBIGUOUS_CHEAP_USEFUL_EVIDENCE",
        "M05_AMBIGUOUS_EXPENSIVE_EVIDENCE",
    ):
        result = by_id[case_id]
        case = case_by_id[case_id]
        print(f"{case_id}: request cost={case['request_cost']} synthetic units; "
              f"Policy 2={result['actions']['Policy 2']}")
    for case_id in (
        "M15A_LOW_REVIEW_COST",
        "M15B_MODERATE_REVIEW_COST",
        "M15C_HIGH_REVIEW_COST",
    ):
        result = by_id[case_id]
        case = case_by_id[case_id]
        print(f"{case_id}: human-review cost={case['human_review_cost']} synthetic units; "
              f"Policy 2={result['actions']['Policy 2']}")
    print("\nObserved matrix pattern:")
    print("Baseline proceeds in every case. Policy 1 follows its 30% threshold and evidence availability.")
    print("Policy 2 compares modeled action costs; it responds to evidence value, request cost,")
    print("wrong-PROCEED cost, and review cost.")
    print("M04/M05: increasing request cost changes Policy 2 from request to proceed.")
    print("M15A/B/C: increasing review cost changes Policy 2 from review to request to proceed.")
    print("M11/M12/M13: at 29% Policy 1 proceeds; at 30% and 31% it requests evidence.")
    print("Evidence availability alone does not set Policy 2's action; uncertainty alone does not either.")
    print("These are observations from designed synthetic cases, not general performance claims.")
    print("C18 - Expanded experiment interpreted")

    print(f"\n{RULE}\nCHECKPOINT\n{RULE}")
    print("C16 - Synthetic case matrix implemented")
    print("\nSTAGE 9 COMPLETE")


def display_break_results(results: list[dict], assessments: dict) -> None:
    print(f"\n{RULE}\nC19 - DELIBERATE SYNTHETIC BREAK TESTS\n{RULE}")
    for result in results:
        actions = result["actions"]
        truth = result["evaluation_only"]["hidden_ground_truth"]
        actual = (f"B={actions['Baseline']}, P1={actions['Policy 1']}, "
                 f"P2={actions['Policy 2']}")
        print(f"\n{result['case_id']} | stressed: {result['stress']}")
        print(f"Expected: {result['expected_behavior']}")
        print(f"Actual: {actual}; posterior concerning="
              f"{result['posterior']['concerning']:.2%}; truth={truth} (evaluation only)")
        costs = result["expected_costs"]
        print(f"Expected costs: B={costs['Baseline']:.2f}, "
              f"P1={costs['Policy 1']:.2f}, P2={costs['Policy 2']:.2f}")
        print(f"Assessment: {assessments[result['case_id']]}")
    print("\nNo policy was changed during break testing.")
    print("C19 - Deliberate break tests complete")

    print(f"\n{RULE}\nC20 - POLICY REFINEMENT REVIEW\n{RULE}")
    print("No policy modification was justified by these tests.")
    print("Observed failures reflect sensitivity to synthetic priors/likelihoods or")
    print("intentional Policy 1 behavior, not a demonstrated defect in cost comparison.")
    print("C20 - Policy refinement reviewed")

    print(f"\n{RULE}\nC21 - WEEK 1 EXPERIMENT COMPLETE\n{RULE}")
    print("Final report: README.md")
    print("C21 - Week 1 experiment complete")
    print("\n=======================================================")
    print("WEEK 1 LOAN AGENT EXPERIMENT COMPLETE")
    print("=======================================================")
