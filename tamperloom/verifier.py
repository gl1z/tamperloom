import json
from pathlib import Path

from tamperloom.schema import _sha256

GENESIS_HASH = "0" * 64


def verify_chain_json(filepath: str) -> dict:
    path = Path(filepath)
    checkpoint = Path(filepath + ".checkpoint")

    if not path.exists():
        if checkpoint.exists():
            return {"valid": False, "message": "log file missing but checkpoint exists — log may have been deleted"}
        return {"valid": False, "message": f"file not found: {filepath}"}

    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    if not entries:
        return {"valid": False, "message": "log is empty"}

    expected_prev = GENESIS_HASH

    for i, entry in enumerate(entries):
        stored_hash = entry.pop("entry_hash")
        recomputed = _sha256(json.dumps(entry, sort_keys=True))

        if recomputed != stored_hash:
            return {"valid": False, "message": f"hash mismatch at entry {i} (id: {entry['id']})"}

        if entry["prev_hash"] != expected_prev:
            return {"valid": False, "message": f"chain broken at entry {i} — prev_hash doesn't match"}

        expected_prev = stored_hash

    if checkpoint.exists():
        saved = checkpoint.read_text().strip()
        if saved != expected_prev:
            return {"valid": False, "message": "checkpoint mismatch — log may have been truncated or replaced"}

    return {"valid": True, "message": f"chain valid: {len(entries)} entries verified"}


def verify_chain(filepath: str) -> bool:
    # keeping this for backwards compatibility
    result = verify_chain_json(filepath)
    print(result["message"])
    return result["valid"]