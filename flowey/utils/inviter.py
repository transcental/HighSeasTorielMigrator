import logging
from slack_sdk.errors import SlackApiError
import asyncio
import traceback
from flowey.utils.env import env

async def invite(user_id: str) -> bool:
    completed = False
    while not completed:
        try:
            user_info = await env.slack_client.users_info(user=user_id)
            mcg: bool = user_info["user"]["is_restricted"]
            if not mcg:
                return False
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after)
            else:
                t_info = traceback.format_exc()
                logging.error(f"Failed to get user info: {e}", exc_info=True)
                while True:
                    try:
                        await env.slack_client.chat_postMessage(channel="U054VC2KM9P", text=f"Failed to get user info: {e}\n```{t_info}```")
                        break
                    except SlackApiError as ef:
                        if e.response["error"] == "ratelimited":
                            retry_after = int(e.response.headers.get("Retry-After", 1))
                            await asyncio.sleep(retry_after)
                        else:
                            logging.error(f"Failed to send error message: {ef}", exc_info=True)
                            break
                completed = True
                return False
    completed = False
    while not completed:
        try:
            await env.slack_client.conversations_invite(
                channel = "C039PAG1AV7",
                users=[user_id],
                token=env.slack_user_token
            )
            completed = True
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after)
            else:
                logging.error(f"Failed to invite user: {e}", exc_info=True)
                completed = True
                return False
                break
    return True