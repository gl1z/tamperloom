import sys
from tamperloom.verifier import verify_chain


def main():
    if len(sys.argv) < 3:
        print("usage: tamperloom verify <path-to-log>")
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]

    if command == "verify":
        valid = verify_chain(filepath)
        sys.exit(0 if valid else 1)
    else:
        print(f"unknown command: {command}")
        sys.exit(1)