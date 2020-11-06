import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep

# Battleground states to watch
states = [
    'Arizona',
    'Georgia',
    'Pennsylvania',
    # for some reason Nevada is causing an error
    # 'Nevada'
]
TIME_INTERVAL = 60  # in seconds, change to how often you want it to update


def check_state(state_url):
    vote_counts = {}
    page = requests.get(state_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='e-table e-results-table')
    body = table.find('tbody')
    trs = body.find_all('tr')
    for tr in trs:
        name = tr.find('span', class_='e-name-display').text
        votes = tr.find('span', class_='e-votes-display').text
        if 'Trump' in name:
            vote_counts['Trump'] = int(votes.replace(',', ''))
        elif 'Biden' in name:
            vote_counts['Biden'] = int(votes.replace(',', ''))
    print('Trump votes:', vote_counts['Trump'])
    print('Biden votes:', vote_counts['Biden'])
    print("Biden's lead:", vote_counts['Biden'] - vote_counts['Trump'])


def check_states():
    print(datetime.now())
    for state in states:
        state_url = f'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-{state.lower()}-president.html'
        print(state)
        check_state(state_url)


while True:
    check_states()
    sleep(TIME_INTERVAL)
