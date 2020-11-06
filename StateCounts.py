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
TIME_INTERVAL = 60 * 5  # in seconds, change to how often you want it to update


def init_vote_counts(states):
    vote_counts = {}
    for state in states:
        vote_counts[state] = {'Trump': 0, 'Biden': 0}
    return vote_counts


def print_votes(state):
    print('VOTE UPDATE')
    print(datetime.now())
    print(state)
    print('Trump votes:', vote_counts[state]['Trump'])
    print('Biden votes:', vote_counts[state]['Biden'])
    print("Biden's lead:",
          vote_counts[state]['Biden'] - vote_counts[state]['Trump'])
    print('\a\a\a')


def check_state(state):
    state_url = f'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-{state.lower()}-president.html'
    page = requests.get(state_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_='e-table e-results-table')
    body = table.find('tbody')
    trs = body.find_all('tr')

    votes_changed = False
    for tr in trs:
        name = tr.find('span', class_='e-name-display').text
        votes_string = tr.find('span', class_='e-votes-display').text
        votes = int(votes_string.replace(',', ''))
        candidate = 'Trump' if 'Trump' in name else 'Biden' if 'Biden' in name else None
        if candidate:
            if vote_counts[state][candidate] != votes:
                votes_changed = True
            vote_counts[state][candidate] = votes
    if votes_changed:
        print_votes(state)


def check_states():
    for state in states:
        check_state(state)


vote_counts = init_vote_counts(states)
while True:
    check_states()
    sleep(TIME_INTERVAL)
