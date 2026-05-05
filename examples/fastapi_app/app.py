from fastapi import FastAPI, Header, Request
from tamperloom.logger import AuditLogger

app = FastAPI()

# same idea as the flask one, single log file for the demo
logger = AuditLogger("audit.jsonl")


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    user = data.get("username", "unknown")

    logger.log(
        event_type="user.login",
        actor=user,
        action="login",
        target="app",
    )

    return {"status": "logged in", "user": user}


@app.delete("/delete/{resource_id}")
async def delete_resource(resource_id: str, x_actor: str = Header(default="unknown")):
    logger.log(
        event_type="resource.deleted",
        actor=x_actor,
        action="delete",
        target=resource_id,
        metadata={"requested_by": x_actor},
    )

    return {"status": "deleted", "id": resource_id}