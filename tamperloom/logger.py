import json
from pathlib import Path

from tamperloom.schema import build_entry

# first entry in a new log has nothing before it
GENESIS_HASH = "0" * 64


class AuditLogger:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self._prev_hash = self._get_last_hash()

    def _get_last_hash(self) -> str:
        # if the file doesn't exist yet, this is a fresh log
        if not self.filepath.exists():
            return GENESIS_HASH

        last_line = None
        with open(self.filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    last_line = line

        if last_line is None:
            return GENESIS_HASH

        # grab the hash from whatever the last entry was
        return json.loads(last_line)["entry_hash"]

    def log(self, event_type: str, actor: str, action: str, target: str, metadata=None):
        entry = build_entry(
            event_type=event_type,
            actor=actor,
            action=action,
            target=target,
            prev_hash=self._prev_hash,
            metadata=metadata,
        )

        with open(self.filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

        # update so the next entry chains off this one
        self._prev_hash = entry["entry_hash"]