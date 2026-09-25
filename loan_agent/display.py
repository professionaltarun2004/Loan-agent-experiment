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


def display_matrix_results(results: list[dict], cases: list[dict]) -> None:
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

    print(f"\n{RULE}\nCHECKPOINT\n{RULE}")
    print("C16 - Synthetic case matrix implemented")
    print("\nSTAGE 9 COMPLETE")
    print("NEXT:")
    print("Run the expanded experiment and inspect policy sensitivity.")
