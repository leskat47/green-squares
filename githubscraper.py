import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from github import get_longest_streak
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'leslie@eagerorange.com',
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    )


mail = Mail(app)

url_base = "https://github.com/"
participants = {"leskat47": {"name": "Leslie", "email": "leslie@eagerorange.com"},
                "lobsterkatie": {"name": "Katie", "email": None},
                "jacquelineawatts": {"name": "Jacqui", "email": None},
                "franziskagoltz": {"name": "Franzi", "email": None},
                "levi006": {"name": "Vi", "email": None},
                "mcbishop": {"name": "Meg", "email": None},
                "allymcknight": {"name": "Ally", "email": None}}


def send_update_note(streak, participant, committed_today):
    """ Send status note and reminder to participants """
    if participant["email"]:
        subject = "Your Green Square Report"
        if not committed_today:
            message = "Hi %s! Don't forget to earn your green square for the day! You're currently at %d days of green squares." % (participant["name"], streak)
        else:
            message = "Hi %s! Good job earning your green square today! You're currently at %d days of green squares." % (participant["name"], streak)
        with app.app_context():
            msg = Message(subject, sender='leslie@eagerorange.com', recipients = [participant["email"]])
            msg.body = message
            mail.send(msg)

    return

def show_squares_data(participants):
    for participant in participants:
        url = requests.get(url_base + participant).text
        soup = BeautifulSoup(url, 'html.parser')
        squares = []
        for square in soup.find_all('rect'):
            if int(square["data-count"]) > 0:
                squares.append(datetime.strptime(square['data-date'], "%Y-%m-%d").date())

        streak = get_longest_streak(squares)
        committed_today = (squares[-1] == date.today())

        send_update_note(streak, participants[participant], committed_today)

        print participant, " ", streak

show_squares_data(participants)
