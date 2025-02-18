from pyairtable import Api
from dotenv import load_dotenv
import os
load_dotenv()
ac = Api(
    api_key=os.getenv("AIRTABLE_API_KEY", ""),
    endpoint_url="https://middleman.hackclub.com/airtable"
)

ut = ac.table(os.getenv("AIRTABLE_BASE_ID", ""), os.getenv("AIRTABLE_TABLE_ID", ""))

users = ut.all(view="[FLOWEY] Non-migrated users", fields=["slack_id"])
print(f"Checking {len(users)} users")

print(users[0])