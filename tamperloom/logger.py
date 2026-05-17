import json
from pathlib import Path

import portalocker

from tamperloom.schema import build_entry

GENESIS_HASH = "0" * 64


class AuditLogger:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.checkpoint = Path(filepath + ".checkpoint")
        self._prev_hash = self._get_last_hash()

    def _get_last_hash(self) -> str:
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

        return json.loads(last_line)["entry_hash"]

    def _update_checkpoint(self, latest_hash: str):
        # keep a separate record of the latest hash
        # if the log gets wiped, this still exists
        with open(self.checkpoint, "w") as f:
            f.write(latest_hash)

    def log(self, event_type: str, actor: str, action: str, target: str, metadata=None):
        entry = build_entry(
            event_type=event_type,
            actor=actor,
            action=action,
            target=target,
            prev_hash=self._prev_hash,
            metadata=metadata,
        )

        # lock the file while writing so concurrent processes don't corrupt the chain
        with open(self.filepath, "a") as f:
            portalocker.lock(f, portalocker.LOCK_EX)
            f.write(json.dumps(entry) + "\n")
            portalocker.unlock(f)

        self._prev_hash = entry["entry_hash"]
        self._update_checkpoint(self._prev_hash)