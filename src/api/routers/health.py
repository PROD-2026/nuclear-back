from litestar import Controller, get


class HealthController(Controller):
    path = "/health"
    tags = ["Health Check"]

    @get("/")
    async def is_healthy(self) -> dict[str, str]:
        return {"message": "Nuclear IT Hack!"}
