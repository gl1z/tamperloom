import json
import pytest
from tamperloom.logger import AuditLogger
from tamperloom.verifier import verify_chain


def test_valid_chain(tmp_path):
    log = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(log))
    logger.log(event_type="user.login", actor="admin", action="login", target="app")
    logger.log(event_type="record.deleted", actor="admin", action="delete", target="rec_1")

    assert verify_chain(str(log)) is True


def test_tampered_entry_fails(tmp_path):
    log = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(log))
    logger.log(event_type="user.login", actor="admin", action="login", target="app")

    # manually edit the log to simulate tampering
    entries = log.read_text().splitlines()
    entry = json.loads(entries[0])
    entry["actor"] = "hacker"
    log.write_text(json.dumps(entry) + "\n")

    assert verify_chain(str(log)) is False


def test_empty_log(tmp_path):
    log = tmp_path / "audit.jsonl"
    log.write_text("")

    assert verify_chain(str(log)) is False


def test_genesis_hash(tmp_path):
    log = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(log))
    logger.log(event_type="test.event", actor="a", action="b", target="c")

    entry = json.loads(log.read_text().splitlines()[0])
    assert entry["prev_hash"] == "0" * 64


def test_chain_links_correctly(tmp_path):
    log = tmp_path / "audit.jsonl"
    logger = AuditLogger(str(log))
    logger.log(event_type="event.one", actor="a", action="b", target="c")
    logger.log(event_type="event.two", actor="a", action="b", target="c")

    entries = [json.loads(line) for line in log.read_text().splitlines()]
    # second entry's prev_hash should match first entry's entry_hash
    assert entries[1]["prev_hash"] == entries[0]["entry_hash"]