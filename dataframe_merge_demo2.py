"""Compare old (truth) and new (candidate) event-driven test results.

Messages describe the event context: a fail can identify a missing response,
while a skip can identify a trigger that the scenario did not produce.
"""

import pandas as pd

RESULT_COLUMNS = ["req_id", "test_id", "scenario", "outcome", "message"]


def build_results(
    results: list[tuple[str, int, str, str, str | None]],
) -> pd.DataFrame:
    """Build result rows, deriving each test ID from its requirement and GLM instance."""
    return pd.DataFrame(
        [
            {
                "req_id": req_id,
                "test_id": f"{req_id}_GLM_{glm_instance}",
                "scenario": scenario,
                "outcome": outcome,
                "message": message,
            }
            for req_id, glm_instance, scenario, outcome, message in results
        ],
        columns=RESULT_COLUMNS,
    )


truth = build_results(
    [
        ("TEx_GWS_001", 1, "baseline", "pass", None),
        ("TEx_GWS_002", 1, "baseline", "pass", None),
        (
            "TEx_GWS_003",
            1,
            "scripted",
            "fail",
            "High-temperature trigger occurred, but the cooling response was not observed.",
        ),
        ("TEx_GWS_004", 1, "scripted", "pass", None),
        ("TEx_GWS_005", 1, "scenario_n", "pass", None),
        ("TEx_GWS_006", 1, "baseline", "pass", None),
        (
            "TEx_GWS_006",
            10,
            "baseline",
            "fail",
            "Low-pressure trigger occurred, but the pump did not start.",
        ),
        ("TEx_GWS_006", 1, "scenario_n", "pass", None),
        ("TEx_GWS_006", 2, "scenario_n", "pass", None),
        ("TEx_GWS_006", 3, "scenario_n", "pass", None),
        ("TEx_GWS_006", 4, "scenario_n", "pass", None),
        ("TEx_GWS_006", 5, "scenario_n", "pass", None),
        ("TEx_GWS_006", 6, "scenario_n", "pass", None),
        ("TEx_GWS_006", 7, "scenario_n", "pass", None),
        ("TEx_GWS_006", 8, "scenario_n", "pass", None),
        (
            "TEx_GWS_007",
            1,
            "baseline",
            "skip",
            "The baseline scenario did not produce the overcurrent trigger.",
        ),
        (
            "TEx_GWS_007",
            10,
            "baseline",
            "skip",
            "The baseline scenario did not produce the overcurrent trigger.",
        ),
    ]
)

candidate = build_results(
    [
        ("TEx_GWS_001", 1, "baseline", "pass", None),
        (
            "TEx_GWS_002",
            1,
            "baseline",
            "fail",
            "Start command trigger occurred, but no running-state response arrived in time.",
        ),
        ("TEx_GWS_003", 1, "scripted", "pass", None),
        ("TEx_GWS_004", 1, "scripted", "pass", None),
        ("TEx_GWS_005", 1, "scenario_n", "error", "Simulation did not converge."),
        ("TEx_GWS_006", 1, "baseline", "pass", None),
        ("TEx_GWS_006", 10, "baseline", "pass", None),
        ("TEx_GWS_006", 1, "scenario_n", "pass", None),
        (
            "TEx_GWS_006",
            2,
            "scenario_n",
            "fail",
            "Low-pressure trigger occurred, but the pump did not start.",
        ),
        ("TEx_GWS_006", 3, "scenario_n", "pass", None),
        ("TEx_GWS_006", 4, "scenario_n", "pass", None),
        ("TEx_GWS_006", 5, "scenario_n", "pass", None),
        ("TEx_GWS_006", 6, "scenario_n", "pass", None),
        ("TEx_GWS_006", 7, "scenario_n", "pass", None),
        ("TEx_GWS_006", 8, "scenario_n", "pass", None),
        (
            "TEx_GWS_007",
            1,
            "baseline",
            "skip",
            "The baseline scenario did not produce the overcurrent trigger.",
        ),
        (
            "TEx_GWS_007",
            10,
            "baseline",
            "skip",
            "The baseline scenario did not produce the overcurrent trigger.",
        ),
    ]
)


if __name__ == "__main__":
    comparison = (
        truth.merge(
            candidate,
            on=["req_id", "test_id", "scenario"],
            how="outer",
            suffixes=("_truth", "_candidate"),
            validate="one_to_one",
            indicator=True,
        )
        .assign(
            outcome_matches=lambda results: results["outcome_truth"]
            == results["outcome_candidate"]
        )
        .sort_values(["req_id", "test_id", "scenario"])
    )

    outputs = {
        "truth": truth,
        "candidate": candidate,
        "comparison": comparison,
    }
    for name, results in outputs.items():
        results.to_csv(f"{name}_results.csv", index=False)
        print(f"Saved {name}_results.csv ({len(results)} rows)")
