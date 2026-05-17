import json
from pathlib import Path

from tamperloom.schema import _sha256

GENESIS_HASH = "0" * 64


def verify_chain(filepath: str) -> bool:
    path = Path(filepath)
    checkpoint = Path(filepath + ".checkpoint")

    if not path.exists():
        # log is gone but checkpoint still exists — someone wiped the log
        if checkpoint.exists():
            print("log file missing but checkpoint exists — log may have been deleted")
            return False
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
        stored_hash = entry.pop("entry_hash")
        recomputed = _sha256(json.dumps(entry, sort_keys=True))

        if recomputed != stored_hash:
            print(f"hash mismatch at entry {i} (id: {entry['id']})")
            return False

        if entry["prev_hash"] != expected_prev:
            print(f"chain broken at entry {i} — prev_hash doesn't match")
            return False

        expected_prev = stored_hash

    # check final hash matches checkpoint
    if checkpoint.exists():
        saved = checkpoint.read_text().strip()
        if saved != expected_prev:
            print("checkpoint mismatch — log may have been truncated or replaced")
            return False

    print(f"chain valid: {len(entries)} entries verified")
    return True