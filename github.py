import requests
from datetime import datetime, timedelta, date
from dateutil import tz

participants = ["leskat47", "lobsterkatie", "jacquelineawatts", "franziskagoltz", "jgriffith23", "levi006", "allymcknight"]
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/Los_Angeles')

r = requests.get("https://api.github.com/users/leskat47/events").json()


def get_user_data(participant):
    """ Get data from github api """

    url = "https://api.github.com/users/" + user + "/events"
    return requests.get(url).json()


def get_dates(user_data):
    """ Get user event dates that include commits """

    dates = []

    for item in user_data:
        if item["payload"].get("commits"):
            for commit in item["payload"]["commits"]:
                commit_data = requests.get(url).json()
                date = datetime.strptime(commit_data["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                dates.append(date)
    # "commit": {
        # "author": {
        #   "name": "Leslie Castellanos",
        #   "email": "lesliekate@gmail.com",
        #   "date": "2016-12-14T07:31:18Z"
        # },
        # "committer": {
        #   "name": "Leslie Castellanos",
        #   "email": "lesliekate@gmail.com",
        #   "date": "2016-12-14T07:31:18Z"
        # },
        # "message": "Pseudocode written",
        # "tree": {
        #   "sha": "8173488cd9182dc303082236bbb8c26b96d993af",
        #   "url": "https://api.github.com/repos/leskat47/green-squares/git/trees/8173488cd9182dc303082236bbb8c26b96d993af"
        # },
        # "url": "https://api.github.com/repos/leskat47/green-squares/git/commits/5c285a3594ad9fed2ebed4113442a478bc8479b4",
        # "comment_count": 0
    return dates


def get_date(user_data, idx):
    date_utc = datetime.strptime(user_data[idx]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    date_utc = date_utc.replace(tzinfo=from_zone)
    date_local = date_utc.astimezone(to_zone).date()
    return date_local

def get_longest_streak(user_data):
    # FIXME: Change to new CORRECT commit dates
    
    # check for commit today or yesterday
    today = date.today()
    event_date = get_date(user_data, 0)

    prev_event_date = get_date(user_data, 1)
    # is the last event today or yesterday?
    if event_date != today and event_date != today - timedelta(days=1):
        return 0

    # if the last event is yesterday, and it has commits
    if event_date == today - timedelta(days=1) and user_data[0]["payload"].get("commits"):
        day_counter = 1
    # if the last event is today but there are no commits, check that yesterday has commits
    elif event_date == today and not user_data[-1]["payload"].get("commits"):
        if prev_event_date == today - timedelta(days=1) and user_data[1]["payload"].get("commits"):
            day_counter = 1
        else:
            return 0
    else:
        day_counter = 1

    # iterate in reverse order
    for i in range(len(user_data) - 1):
        if not user_data[i]["payload"].get("commits"):
            return day_counter
        # Compare to date minus one day using datetime
        if get_date(user_data, i) == get_date(user_data, i - 1 ) - timedelta(days=1):
            day_counter += 1

    return day_counter

user_streaks = {}
for user in participants:
    print user
    data = get_user_data(user)
    print get_longest_streak(data)

    # get length of streak
    # Add user to dictionary,
