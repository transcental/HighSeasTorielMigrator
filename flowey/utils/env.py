import os
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()

class Environment:
    def __init__(self):
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "unset")
        self.slack_user_token = os.environ.get("SLACK_USER_TOKEN", "unset")
        self.slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "unset")

        self.airtable_api_key = os.environ.get("AIRTABLE_API_KEY", "unset")
        self.airtable_base_id = os.environ.get("AIRTABLE_BASE_ID", "unset")
        self.airtable_table_id = os.environ.get("AIRTABLE_TABLE_ID", "unset")
        self.airtable_arcade_base_id = os.environ.get("AIRTABLE_ARCADE_BASE_ID", "unset")
        self.airtable_arcade_table_id = os.environ.get("AIRTABLE_ARCADE_TABLE_ID", "unset")

        unset = [key for key, value in vars(self).items() if value == "unset"]
        if unset:
            raise ValueError(f"Environment variables not set: {', '.join(unset).upper()}")

        self.port = int(os.environ.get("PORT", 3000))
        self.slack_client = AsyncWebClient(token=self.slack_bot_token)

env = Environment()