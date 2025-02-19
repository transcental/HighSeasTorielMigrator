import asyncio
import logging
import traceback
from slack_sdk.errors import SlackApiError
from flowey.utils.env import env

async def message(user_id: str):
    done = False
    while not done:
        try:
            await env.slack_client.chat_postMessage(
                channel=user_id,
                text="Howdy! I'm Flowey. Flowey the Flower!\n\nAs one of TORIEL's closest friends, I'm here to help you get upgraded to a full member now that the High Seas have drained leaving an empty backroom behind.\n*Stumble into <#C039PAG1AV7> to continue.* If you get stuck, feel free to message <@U054VC2KM9P> or email slack@hackclub.com!"
            )
            done = True
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after)
            else:
                raise e
                done = True
            continue

async def fix_message(user_id: str):
    completed = False
    while not completed:
        try:
            user_info = await env.slack_client.users_info(user=user_id)
            mcg: bool = user_info["user"].get("is_restricted", False)
            if not mcg:
                return False
            completed = True
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                logging.info("User info ratelimited")
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
    done = False
    while not done:
        try:
            await env.slack_client.chat_postMessage(
                channel=user_id,
                text="Howdy! It looks like Flowey did a goof and linked the wrong channel!.\nYou should *stumble into <#C039PAG1AV7> to continue.* If you get stuck, please message <@U054VC2KM9P> or email slack@hackclub.com!"
            )
            done = True
        except SlackApiError as e:
            if e.response["error"] == "ratelimited":
                retry_after = int(e.response.headers.get("Retry-After", 1))
                await asyncio.sleep(retry_after)
            else:
                raise e
                done = True
            continue
