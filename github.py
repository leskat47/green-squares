import requests

participants = ["leskat47", "lobsterkatie", "jacquelineawatts", "franziskagoltz", "jgriffith23", "levi006", "allymcknight"]


r = requests.get("https://api.github.com/users/leskat47/events").json()

dates = []

for item in r:
    if item["payload"].get("commits"):
        dates.append(item["created_at"])

print sorted(dates)
