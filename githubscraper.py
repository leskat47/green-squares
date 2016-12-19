from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta, date
from github import get_longest_streak


url_base = "https://github.com/"


participants = ["leskat47", "lobsterkatie", "jacquelineawatts", "franziskagoltz", "levi006", "allymcknight"]

def show_squares_data(participants):
    for participant in participants:
        url = requests.get(url_base + participant).text
        soup = BeautifulSoup(url, 'html.parser')
        squares = []
        for square in soup.find_all('rect'):
            if int(square["data-count"]) > 0:
                squares.append(datetime.strptime(square['data-date'], "%Y-%m-%d").date())

        print participant, " ", get_longest_streak(squares)

show_squares_data(participants)
