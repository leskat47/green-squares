import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from github import get_longest_streak
from flask import Flask
from flask_mail import Mail, Message


def send_update_note(participant):
    """ Send status note and reminder to participants """

    subject = "Your Green Square Report"
    if not participant["committed_today"]:
        message = "Hi %s! Don't forget to earn your green square for the day! You're currently at %d days of green squares." % (participant["name"], participant["streak"])
    else:
        message = "Hi %s! Good job earning your green square today! You're currently at %d days of green squares." % (participant["name"], participant["streak"])
    with app.app_context():
        msg = Message(subject, sender='greensquarechallenge@gmail.com', recipients = [participant["email"]])
        msg.body = message
        mail.send(msg)

    return


def get_date_squares(url_base, participant):
    """ Return list of consecutive squares dates for a participant from scraped data """

    url = requests.get(url_base + participant).text
    soup = BeautifulSoup(url, 'html.parser')
    squares = []
    for square in soup.find_all('rect'):
        if int(square["data-count"]) > 0:
            squares.append(datetime.strptime(square['data-date'], "%Y-%m-%d").date())
    return squares


def update_participant_status():
    """ Run status check and update user by email """

    url_base = "https://github.com/"
    participants = [{"id": "leskat47", "name": "Leslie", "email": "leslie@eagerorange.com"},
                    {"id": "lobsterkatie", "name": "Katie", "email": None},
                    {"id": "jacquelineawatts", "name": "Jacqui", "email": None},
                    {"id": "franziskagoltz", "name": "Franzi", "email": None},
                    {"id": "levi006", "name": "Vi", "email": None},
                    {"id": "mcbishop", "name": "Meg", "email": None},
                    {"id": "allymcknight", "name": "Ally", "email": None}]
    for participant in participants:
        dates = get_date_squares(url_base, participant["id"])
        participant["committed_today"] = (dates[-1] == date.today())
        participant["streak"] = get_longest_streak(dates)
        if participant["email"]:
            send_update_note(participant)


if __name__ == "__main__":

    app = Flask(__name__)
    app.config.update(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_SSL=False,
        MAIL_USE_TLS=True,
        MAIL_USERNAME = 'greensquarechallenge@gmail.com',
        MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
        )

    mail = Mail(app)
    update_participant_status()
