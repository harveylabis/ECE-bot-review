### THIS FILE SCRAPES THE QUESTIONS, CHOICES, ANSWER, AND IMAGE URL (if present) ###

from bs4 import BeautifulSoup
import requests
import re
import json
from time import sleep

# define the regex patterns
que_pattern = "[0-9]+\. " # pattern for question
choi_pattern = "[ABCD]\) |[ABCD]\. " # pattern for choices with letter+parenthesis: pattern 1
img_pattern = "(http.+?\.png)|(http.+?\.gif)" # pattern for links of image attached: png

# open the topics
with open("queLinks.json", 'r') as f:
    topics_urls = json.load(f)
topics = [topic for topic in topics_urls]

# loop through topics
for topic in topics:
    filename = topic + ".json"
    que_count = 1
    links_count = 1

    contents = {}
    # loop through urls inside a current topic
    for url in topics_urls[topic]["urls"]:
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        item = {}
        item["choices"] = []
        item_with_url = False
        question_found = False

        # loop through the lines (view source)
        # <p> - question, choices ; <a> - img link
        for line in soup:
            line_str = str(line)

            que_found = re.search(que_pattern, line_str)
            img_found = re.search(img_pattern, line_str)
            choi_found = re.search(choi_pattern, line_str)
            key_found = "Option" in line_str

            if que_found:
                question = line.text # .replace(que_found.group(), "")
                item["question"] = question
                question_found = True
            
            elif img_found and question_found:
                item_with_url = True
                item["url"] = img_found[0]

            elif choi_found:
                choice = line.text
                if ")" in choice:
                    choice = choice.replace(")", ".")
                item["choices"].append(choice)

            elif key_found:
                item["key"] = line.text
                item["id"] = que_count
                if not item_with_url:
                    item["url"] = None
                contents[que_count] = item.copy()
                
                # reset variables
                item["choices"] = []
                que_count += 1
                item["url"] = None
                item_with_url = False
                question_found = False

# MAKE A MODULAR FUNCTION

    with open(filename, 'w', encoding="utf8") as f:
        json.dump(contents, f, indent=2, ensure_ascii=False)
