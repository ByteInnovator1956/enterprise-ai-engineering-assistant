import sys

from analyzer.app import answer_question

def main():
    question = " ".join(sys.argv[1:])

    if not question:
        print("Please provide a question.")
        return

    result = answer_question(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nEvidence:")
    for item in result["evidence"].items:
        location = item.file

        if (
            item.start_line is not None
            and item.end_line is not None
        ):
            location += f":{item.start_line}-{item.end_line}"

        print(f"- {item.type}: {location}")

if __name__ == "__main__":
    main()