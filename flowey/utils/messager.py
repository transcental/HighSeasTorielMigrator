import asyncio
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
