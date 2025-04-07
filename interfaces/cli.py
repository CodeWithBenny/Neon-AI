import argparse
from core import AICodingAssistant


def main():
    assistant = AICodingAssistant()
    parser = argparse.ArgumentParser(description="AI Coding Assistant CLI")

    subparsers = parser.add_subparsers(dest="command")

    # Complete command
    complete_parser = subparsers.add_parser("complete")
    complete_parser.add_argument("code", help="Partial code to complete")
    complete_parser.add_argument("-l", "--language", default="python")

    # Debug command
    debug_parser = subparsers.add_parser("debug")
    debug_parser.add_argument("code", help="Code with error")
    debug_parser.add_argument("error", help="Error message")
    debug_parser.add_argument("-l", "--language", default="python")

    args = parser.parse_args()

    if args.command == "complete":
        print(assistant.completer.complete(args.code, args.language))
    elif args.command == "debug":
        print(assistant.debugger.analyze(args.code, args.error, args.language))


if __name__ == "__main__":
    main()