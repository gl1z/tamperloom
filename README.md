# Tamperloom

Verifiable append-only audit logs for Python apps and agents.

## The problem

Standard logs don't prove integrity. Anyone with access to the file or 
database can edit, delete, or insert entries and leave no trace.

## What this does

Every entry Tamperloom writes is cryptographically linked to the one 
before it. If anything is changed after the fact, the verifier catches 
it and tells you which entry broke the chain.

Entries are stored as JSONL — one per line, no database required.

## Install

```bash
pip install tamperloom
```

## Quick start

```python
from tamperloom import AuditLogger

logger = AuditLogger("audit.jsonl")
logger.log(
    event_type="user.role_changed",
    actor="admin_42",
    action="promote_user",
    target="user_18",
    metadata={"old_role": "member", "new_role": "moderator"}
)
```

## Verify the log

```bash
tamperloom verify audit.jsonl
# chain valid: 1 entries verified
```

## What happens when someone tampers with it

```bash
# edit any value in audit.jsonl manually, then run:
tamperloom verify audit.jsonl
# hash mismatch at entry 0 (id: bde6a704-9e85-41bb-ad25-8125e4bc4ccd)
```

## How it works

Each log entry contains a hash of itself plus the hash of the previous entry. This creates a chain — you can't silently edit any entry without breaking every hash that follows it.

The first entry uses a genesis hash of 64 zeros as its `prev_hash`.

## Framework examples

- `examples/flask_app/` — Flask REST API with audit logging on login and delete endpoints
- `examples/fastapi_app/` — Same thing with FastAPI and uvicorn

## Use cases

- Admin action logging
- Permission and role changes
- Record deletions
- API key creation and revocation
- AI agent tool calls and policy denials

## License

MIT