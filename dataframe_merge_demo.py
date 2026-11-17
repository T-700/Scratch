"""Demonstrate pandas.DataFrame.merge with common join types."""

import pandas as pd


employees = pd.DataFrame(
    {
        "employee_id": [1, 2, 3, 4],
        "name": ["Avery", "Blake", "Casey", "Drew"],
        "department_id": [10, 20, 20, 40],
        "location": ["New York", "Seattle", "Seattle", "Austin"],
    }
)

departments = pd.DataFrame(
    {
        "department_id": [10, 20, 30],
        "department": ["Sales", "Engineering", "Marketing"],
        "location": ["New York", "San Francisco", "Chicago"],
    }
)


if __name__ == '__main__':
    print('left')
    print(employees)
    print('right')
    print(departments)
    for join_type in ("inner", "left", "right", "outer"):
        merged = employees.merge(
            departments,
            on="department_id",
            how=join_type,
            suffixes=("_employee", "_department"),
            indicator=True,
            validate="many_to_one",
        )
        merged = merged.sort_values("department_id", na_position="last")

        print(f"\n{join_type.upper()} JOIN")
        print(merged.to_string(index=False))
