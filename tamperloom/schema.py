import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any


def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def build_entry(
    event_type: str,
    actor: str,
    action: str,
    target: str,
    prev_hash: str,
    metadata: dict[str, Any] | None = None,
) -> dict:
    # build the entry first without the hash
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "actor": actor,
        "action": action,
        "target": target,
        "metadata": metadata or {},
        "prev_hash": prev_hash,
    }

    # hash goes in last so it covers everything including prev_hash
    # sort_keys so the output is always the same regardless of insertion order
    entry["entry_hash"] = _sha256(json.dumps(entry, sort_keys=True))
    return entry