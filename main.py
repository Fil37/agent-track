"""Command-line entry point."""

import argparse

from agent import create_supervisor


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local Agent Track.")
    parser.add_argument("question", help="Question for the supervisor agent")
    args = parser.parse_args()

    result = create_supervisor().invoke(
        {"messages": [("user", args.question)]}
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
