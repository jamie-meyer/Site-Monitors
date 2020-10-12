#
# Usage: python bucks_monitor.py
#

from bs4 import BeautifulSoup
import requests


###
#  LOGIC
###

def main():
    url = 'https://www.ubereats.com/los-angeles/food-delivery/salt-%26-straw-arts-district/ZNBuxm20QeK5MgVPzmgx-w'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.ubereats.com/los-angeles/food-delivery/salt-%26-straw-arts-district/ZNBuxm20QeK5MgVPzmgx-w',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers'
    }
    webhook = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'

    curr_items = read_file('salt_straw.txt')

    response_html = requests.get(url, timeout=5, headers=headers).content
    print(response_html)
    response = BeautifulSoup(response_html, features='lxml')

    pints = response.find_all('ul')[1].find('ul').find_all('li')

    for pint in pints:
        desc = ''.join(title(pint))
        if "birthday" in desc and "sold out" not in desc and len(curr_items) == 0:
            notify("Birthday Cakes & Blackberries back in stock -- Uber Eats", webhook)
            append_to_file('salt_straw.txt', "birthday cakes added!!!!!")
            break


###
#  UTIL
###

def title(pint):
    stripped = [text.lower() for text in pint.stripped_strings]
    return stripped


def notify(description, webhook):
    slack_data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": description,
                }
            }
        ]
    }
    # Sends data to webhook with image and title
    requests.post(webhook, json=slack_data, headers={'Content-Type': 'application/json'})


def read_file(filename):
    with open(filename, 'r') as file:
        arr = file.readlines()
        return [x.replace('\n', '') for x in arr]


def append_to_file(filename, string):
    with open(filename, 'a') as file:
        file.write(string + '\n')


def rewrite_file(filename, lines_list):
    with open(filename, 'w+') as file:
        for line in lines_list:
            file.write(line + '\n')


###
# START
###

if __name__ == '__main__':
    main()
