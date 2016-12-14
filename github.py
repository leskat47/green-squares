import requests
import datetime

participants = ["leskat47", "lobsterkatie", "jacquelineawatts", "franziskagoltz", "jgriffith23", "levi006", "allymcknight"]


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
            dates.append(item["created_at"])

    return dates

def get_longest_streak(user_data):

    # check for commit today or yesterday
    today = datetime.today().date()
    event_date = datetime.strptime(user_data[-1]["created_at"], "%Y-%m-%dT%H:%M:%SZ").date
    if event_date != today and event_date != today - timedelta(days=1):
        return 0

    # iterate in reverse order
    day_counter = 1

    for i in range(len(user_data), 0 -1):
        # Iterate backward over dates, keep counter
        # Compare to date minus one day using datetime
        # Stop if missed date, return counter
        # Date format: datetime.strptime(max(dates), "%Y-%m-%dT%H:%M:%SZ")

user_streaks = {}
for user in participants:
    data = get_user_data(user)
    # get length of streak
    # Add user to dictionary,
