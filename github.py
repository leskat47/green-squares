import requests
from datetime import datetime, timedelta, date
from dateutil import tz
import os

participants = ["leskat47", "lobsterkatie", "jacquelineawatts", "franziskagoltz", "", "levi006", "allymcknight"]
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/Los_Angeles')

token = os.environ["PERSONALACCESSTOKEN"]
headers = {'Authorization': 'token %s' % token}

r = requests.get("https://api.github.com/users/leskat47/events", headers=headers).json()

# Rate limit, register app and authenticate:
# https://developer.github.com/guides/basics-of-authentication/


def get_user_data(participant):
    """ Get data from github api """

    url = "https://api.github.com/users/" + participant + "/events"
    return requests.get(url, headers=headers).json()


def get_dates(user_data):
    """ Get user event dates that include commits """

    dates = []

    for item in user_data:
        if item["payload"].get("commits"):
            for commit in item["payload"]["commits"]:
                commit_data = requests.get(commit["url"], headers=headers).json()
                date = datetime.strptime(commit_data["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                date = convert_date(date)
                dates.append(date)
    dates = sorted(set(dates), reverse=True)

    return dates


def convert_date(date_utc):
    date_utc = date_utc.replace(tzinfo=from_zone)
    date_local = date_utc.astimezone(to_zone).date()
    return date_local

def get_longest_streak(dates):

    # check for commit today or yesterday
    today = date.today()
    event_date = dates[0]

    # is the most recent event today or yesterday?
    if event_date != today and event_date != today - timedelta(days=1):
        return 0

    day_counter = 0
    if dates:
        day_counter = 1

    for i in range(len(dates) - 1):
        # Compare to date minus one day using datetime
        if dates[i] == dates[i + 1] + timedelta(days=1):
            day_counter += 1
        else:
            return day_counter

    return day_counter

user_streaks = {}
for user in participants:
    print user
    data = get_user_data(user)
    dates = get_dates(data)
    print user, " ", get_longest_streak(dates)

    # get length of streak
    # Add user to dictionary,
