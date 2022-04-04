import requests
import json
from fake_useragent import UserAgent

Agent = UserAgent()
browser_header = {"User-Agent": Agent.random}
for states in range(1, 40):
    print("State Code: ", states)
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{states}",
                            headers=browser_header)
    json_data = json.loads(response.text)
    for state in json_data["districts"]:
        print(state["district_id"], '\t', state["district_name"])
    print("\n")
