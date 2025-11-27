import argparse
import sys
from summarization_lib import summarize_text, summarize_pdf, SummaryStyle


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI content summarizer using Amazon Bedrock (Claude)."
    )

    parser.add_argument(
        "--style",
        type=str,
        default="bullet_points",
        choices=["brief", "detailed", "bullet_points", "executive"],
        help="Summary style"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Path to input file (PDF or text file)"
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read input from stdin (e.g., cat file | cli_summarizer.py --stdin)"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.stdin:
        # Read everything piped from stdin
        input_text = sys.stdin.read()
        if not input_text.strip():
            print("No input received from stdin.")
            sys.exit(1)

        summary = summarize_text(input_text, style=args.style)  # type: ignore
        print("\n--- SUMMARY ---\n")
        print(summary)
        return

    if args.file:
        if args.file.lower().endswith(".pdf"):
            summary = summarize_pdf(args.file, style=args.style)  # type: ignore
        else:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
            summary = summarize_text(text, style=args.style)  # type: ignore

        print("\n--- SUMMARY ---\n")
        print(summary)
        return

    print("Please provide either --stdin or --file")
    sys.exit(1)


if __name__ == "__main__":
    main()
