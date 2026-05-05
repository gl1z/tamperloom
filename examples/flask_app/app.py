from flask import Flask, request, jsonify
from tamperloom.logger import AuditLogger

app = Flask(__name__)

# using a single log file for the demo, would be per-user or per-service in a real app
logger = AuditLogger("audit.jsonl")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = data.get("username", "unknown")

    # log it before we do anything else
    logger.log(
        event_type="user.login",
        actor=user,
        action="login",
        target="app",
    )

    return jsonify({"status": "logged in", "user": user})


@app.route("/delete/<resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    actor = request.headers.get("X-Actor", "unknown")

    logger.log(
        event_type="resource.deleted",
        actor=actor,
        action="delete",
        target=resource_id,
        metadata={"requested_by": actor},
    )

    return jsonify({"status": "deleted", "id": resource_id})


if __name__ == "__main__":
    app.run(debug=True)