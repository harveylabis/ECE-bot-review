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

    # loop through urls inside a current topic
    for url in topics_urls[topic]["urls"]:
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, 'html.parser')

        # loop through the lines (view source)
        # <p> - question, choices ; <a> - img link
        for line in soup.find_all(['p', 'a']): 
            img_found = re.search(img_pattern, str(line))
            if re.search(que_pattern, str(line)):
                print("question:", line.text)
            elif img_found:
                print("image:", img_found[0])    
            elif re.search(choi_pattern, str(line)):
                print("choice:", line.text)
    