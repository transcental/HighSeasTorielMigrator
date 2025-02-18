import asyncio
import contextlib
from slack_bolt.async_app import AsyncApp
from starlette.applications import Starlette

from flowey.utils import env
from flowey.utils.loop import check_users


app = AsyncApp(
    token = env.slack_bot_token,
    signing_secret = env.slack_signing_secret
)

@contextlib.asynccontextmanager
async def main(_app: Starlette):
    asyncio.create_task(check_users())
    yield