from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

import flowey.utils
main = flowey.utils.main
slack_app = flowey.utils.slack_app

req_handler = AsyncSlackRequestHandler(slack_app)


async def endpoint(req: Request):
    return await req_handler.handle(req)


app = Starlette(
    debug=True,
    routes=[
        Route(path="/slack/events", endpoint=endpoint, methods=["POST"]),
    ],
    lifespan=main,
)
