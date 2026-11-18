
"""Architecture test.

Vérifie que tous les appels à to_csv dans formation_mlops_2
utilisent explicitement index=False.
"""

import ast
from pathlib import Path

PACKAGE_ROOT = Path(__file__).parents[2] / "formation_mlops_2"


def test_to_csv_called_with_index_false():
    # Given
    errors = []

    # When
    for file in PACKAGE_ROOT.rglob("*.py"):
        tree = ast.parse(file.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if not isinstance(node.func, ast.Attribute):
                continue

            if node.func.attr != "to_csv":
                continue

            has_index_false = any(
                keyword.arg == "index"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is False
                for keyword in node.keywords
            )

            if not has_index_false:
                errors.append(f"{file}:{node.lineno}")

    # Then
    assert not errors, (
        "Appels à to_csv sans index=False :\n"
        + "\n".join(errors)
    )
