import sys
import json
from tamperloom.verifier import verify_chain_json


def main():
    if len(sys.argv) < 3:
        print("usage: tamperloom verify <path-to-log> [--json]")
        sys.exit(1)

    command = sys.argv[1]
    filepath = sys.argv[2]
    as_json = "--json" in sys.argv

    if command == "verify":
        result = verify_chain_json(filepath)

        if as_json:
            print(json.dumps(result))
        else:
            print(result["message"])

        sys.exit(0 if result["valid"] else 1)
    else:
        print(f"unknown command: {command}")
        sys.exit(1)