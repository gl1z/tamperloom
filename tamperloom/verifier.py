import json
from pathlib import Path

from tamperloom.schema import _sha256

GENESIS_HASH = "0" * 64


def verify_chain(filepath: str) -> bool:
    path = Path(filepath)

    if not path.exists():
        print(f"file not found: {filepath}")
        return False

    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    if not entries:
        print("log is empty")
        return False

    expected_prev = GENESIS_HASH

    for i, entry in enumerate(entries):
        # pull the stored hash out before we recompute
        stored_hash = entry.pop("entry_hash")

        recomputed = _sha256(json.dumps(entry, sort_keys=True))

        if recomputed != stored_hash:
            print(f"hash mismatch at entry {i} (id: {entry['id']})")
            return False

        if entry["prev_hash"] != expected_prev:
            print(f"chain broken at entry {i} — prev_hash doesn't match")
            return False

        expected_prev = stored_hash

    print(f"chain valid: {len(entries)} entries verified")
    return True