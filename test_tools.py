import pytest

from tools import evaluate_expression


def test_evaluate_expression_handles_arithmetic() -> None:
    assert evaluate_expression("(25 * 300) / 100") == 75


@pytest.mark.parametrize(
    "expression",
    [
        "__import__('os').system('echo unsafe')",
        "2 ** 100",
        "",
    ],
)
def test_evaluate_expression_rejects_unsupported_input(expression: str) -> None:
    with pytest.raises((SyntaxError, ValueError)):
        evaluate_expression(expression)
