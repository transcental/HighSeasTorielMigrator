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
    logging.info(f"Checking {len(users)} users")
    for user in users:
        logging.info(f"Checking {user['id']}")
        slack_id = user.get("fields", {}).get("slack_id", "")
        if not slack_id:
            logging.info("No slack_id found for user", user['id'])
            continue
        invited = await invite(slack_id)
        if invited:
            logging.info(f"Invited {slack_id}, messaging")
            await message(slack_id)
            while True:
                try:
                    ut.update(user["id"], {"migrated_to_toriel": True})
                    break
                except:
                    logging.error("Failed to update user", user["id"])
                    await asyncio.sleep(0.5)
            logging.info(f"Migrated {slack_id}")
        else:
            logging.info(f"Failed to invite {slack_id}")
        await asyncio.sleep(1)