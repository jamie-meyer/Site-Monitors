#
# Usage: python marine_layer_monitor.py
#

import pickle

from bs4 import BeautifulSoup
import requests


###
#  LOGIC
###

def main():
    url = 'https://www.marinelayer.com/sitemap_products_1.xml?from=1759151233&to=4390419005514'
    response_xml = requests.get(url).content                    # Get XML content
    response = BeautifulSoup(response_xml, features='xml')      # Parse XML with BeautifulSoup
    items = response.find_all('image')                    # Returns array of all item names with tag

    # write_to_pickle_file('marine_layer_items.txt', [])  # Must run this if file is malformed (and take out post request)

    curr_items = read_pickle_file('marine_layer_items.txt')
    all_items = []
    for item in items:
        arr = item.text.split('\n')
        img = arr[1]                                      # Image URL
        title = arr[2]                                    # Name of the item
        all_items.append((img, title))                    # Add all (image, title) pairs  to a list
        if (img, title) not in curr_items:
            slack_data = {
                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "New Item Found: <" + img + "|" + title + ">",
                                    },
                                    "accessory": {
                                        "type": "image",
                                        "image_url": img,
                                        "alt_text": title
                                    }
                                }
                            ]
                          }
            # Sends data to webhook with image and title
            requests.post('https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX',
                          json=slack_data, headers={'Content-Type': 'application/json'})
    write_to_pickle_file('marine_layer_items.txt', all_items)


###
#  UTIL
###

def read_pickle_file(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


def write_to_pickle_file(filename, an_object):
    with open(filename, 'wb') as file:
        pickle.dump(an_object, file)


###
# START
###

if __name__ == '__main__':
    main()
