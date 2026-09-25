"""Concise terminal presentation for the experiment results."""


RULE = "-" * 55


def display_results(results: list[dict]) -> None:
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

    print(f"\n{RULE}\nCASE DETAILS\n{RULE}")
    for result in results:
        print(f"\n{result['case_id']}")
        print(f"Posterior: legitimate={result['posterior']['legitimate']:.2%}, "
              f"concerning={result['posterior']['concerning']:.2%}")
        print("Actions and expected costs:")
        for policy_name in ("Baseline", "Policy 1", "Policy 2"):
            print(f"  {policy_name:<10} {result['actions'][policy_name]:<18} "
                  f"{result['expected_costs'][policy_name]:.2f}")

    print(f"\n{RULE}\nCHECKPOINT\n{RULE}")
    print("C13 - Policy actions across controlled cases")

    print("\n" + "=" * 55)
    print("STAGE 7R COMPLETE")
    print("=" * 55)
    print("The experiment has been split into modules.")
    print("\nCurrent structure:")
    print("Bayesian reasoning -> bayesian.py")
    print("Policies -> policies.py")
    print("Costs -> costs.py")
    print("Cases -> cases.py")
    print("Evaluation -> evaluation.py")
    print("Display -> display.py")
    print("Runner -> loan_agent_experiment.py")
    print("\nThe experiment logic and synthetic assumptions were preserved.")
    print("\nNext stage:")
    print("evaluate correctness and total decision cost across the policies.")
