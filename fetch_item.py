"""FETCH QUESTIONS, CHOICES, AND KEY ANSWER WITH GIVEN ID
This program will fetch an item from questions in json file, given question id.

author: pororomero
created: 7/18/2021
"""

import json
import sys

topics_links_filename = "queLinks.json"

def open_a_file(filename):
    try:
        with open(filename, 'r') as f:
            topic_urls = json.load(f)
    except FileNotFoundError:
        print(f"The file, {topics_links_filename}, does not exist.")
        print("Program will exit...")
        sys.exit(1) # error
    else:
        data = [topic for topic in topic_urls] # currently supports 5 topics only
        return data

def get_item(id):
    id_items = []
    topics = open_a_file(topics_links_filename)
    for topic in topics:
        # trying to open a file:
        filename = topic + ".json"
        try:
            with open(filename, 'r', encoding="utf8") as f:
                contents = json.load(f)
        except FileNotFoundError:
            print(f"The file, {filename}, does not exist.")
            print("Program will exit...")
        else:
            question = contents[id]["question"]
            choices = contents[id]["choices"]
            key_ans = contents[id]["key"]

            item = topic, question, choices, key_ans
        
        id_items.append(item)

    return id_items

print(get_item(str(1)))
