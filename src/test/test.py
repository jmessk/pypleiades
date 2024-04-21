import requests

file = { "file": ("input.txt", "sample") }

response = requests.post("https://mecrm.dolylab.cc/api/v0.5/data", files=file)

if response.json().get("status"):
    print(response.json())
    data_id = response.json().get("id")

response = requests.get(f"https://mecrm.dolylab.cc/api/v0.5/data/{data_id}/blob")
print(response.text)