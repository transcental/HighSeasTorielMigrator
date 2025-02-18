import asyncio
import contextlib
from slack_bolt.async_app import AsyncApp
from starlette.applications import Starlette

import flowey.utils

env = flowey.utils.env
check_users = flowey.utils.check_users

app = AsyncApp(
    token = env.slack_bot_token,
    signing_secret = env.slack_signing_secret
)

@contextlib.asynccontextmanager
async def main(_app: Starlette):
    asyncio.create_task(check_users())
    yield