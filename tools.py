"""Public RSS retrieval and a restricted arithmetic tool."""

import ast
import json
import math
import operator
import os
from urllib.parse import quote

import feedparser
from langchain_core.tools import tool


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def evaluate_expression(expression: str) -> float:
    """Evaluate bounded arithmetic without executing arbitrary Python code."""
    if not expression.strip() or len(expression) > 100:
        raise ValueError("Provide a non-empty expression of at most 100 characters.")

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
        ):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 10:
                raise ValueError("Exponent magnitude must not exceed 10.")
            return _BINARY_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Only numeric literals and basic arithmetic are supported.")

    value = evaluate(ast.parse(expression, mode="eval"))
    if not math.isfinite(value):
        raise ValueError("The expression must produce a finite result.")
    return value


@tool
def calculate(expression: str) -> str:
    """Calculate a basic arithmetic expression without evaluating Python code."""
    try:
        return json.dumps({"result": evaluate_expression(expression)})
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as error:
        return json.dumps({"error": str(error)}, ensure_ascii=False)


@tool
def latest_youtube_uploads(limit: int = 3) -> str:
    """Return recent uploads from the configured public YouTube channel RSS feed."""
    channel_id = os.getenv("YOUTUBE_CHANNEL_ID", "").strip()
    if not channel_id:
        return json.dumps(
            {"error": "YOUTUBE_CHANNEL_ID is not configured."},
            ensure_ascii=False,
        )
    if not 1 <= limit <= 10:
        return json.dumps({"error": "limit must be between 1 and 10."})

    feed_url = (
        "https://www.youtube.com/feeds/videos.xml?channel_id="
        + quote(channel_id, safe="")
    )
    feed = feedparser.parse(feed_url)
    if feed.bozo and not feed.entries:
        return json.dumps(
            {"error": f"YouTube RSS retrieval failed: {feed.bozo_exception}"},
            ensure_ascii=False,
        )

    return json.dumps(
        [
            {
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
            }
            for entry in feed.entries[:limit]
        ],
        ensure_ascii=False,
    )
