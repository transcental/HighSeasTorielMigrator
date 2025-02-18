import asyncio
from pyairtable import Api
import logging
from flowey.utils.env import env
from flowey.utils.inviter import invite
from flowey.utils.messager import message

ac = Api(
    api_key=env.airtable_api_key,
    endpoint_url="https://middleman.hackclub.com/airtable"
)

ut = ac.table(env.airtable_base_id, env.airtable_table_id)

async def check_users():
    users = ut.all(view="[FLOWEY] Non-migrated users", fields=["slack_id"])
    for user in users:
        slack_id = user.get("fields", {}).get("slack_id", "")
        if not slack_id:
            continue
        invited = await invite(slack_id)
        if invited:
            await message(slack_id)
        ut.update(user["id"], {"migrated_to_toriel": True})
        logging.info(f"Migrated {slack_id}")
        await asyncio.sleep(1)