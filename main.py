"""LOG IN AND SEND THE QUESTION, CHOICES, AND ANSWER; MAIN DRIVER PROGRAM
A program the periodically message an ECE-related questions to Facebook
group chat using 'fbchat' module.

author: pororomero
created: 7/18/2021
"""

import credentials
import json
import fbchat
from fbchat import Client
from fbchat.models import *
import fetch_item
from time import sleep
import re

# log in details
username = credentials.getEmail()
password = credentials.getPassword()
chatIDs = credentials.getChatID()
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" # old user agent
# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36" # new user agent - failed

# cookies stuff here to avoid frequent log in
cookies = {}
try:
    # load the session cookies (if available)
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, we'll just log in again
    pass

# Attempt a log in with session, and if it fails, just use the username and password
client = Client(username, password, max_tries=2, user_agent=user_agent, session_cookies=cookies)
# make sure if log in successfully
if not client.isLoggedIn():
    client.login(username, password)

# saving the cookies
with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)

# get questions and answers
question_count = 1
items = fetch_item.get_item(str(question_count))

for item in items:
    topic = item[0]
    question = item[1]
    choices = item[2]
    key_ans = item[3]

    print("Sending quest:", question)
    client.send(Message(text=topic + "\n" + question), thread_id=chatIDs, thread_type=ThreadType.USER) # send question
    sleep(3)

    for choice in choices:
        print("Sending choic:", choice)
        client.send(Message(text=choice), thread_id=chatIDs, thread_type=ThreadType.USER) # send choices
        sleep(2)

    # after 5 sec for testing, send the answer key
    sleep(5)
    client.send(Message(text=key_ans), thread_id=chatIDs, thread_type=ThreadType.USER) # send key answer

    # wait for 10 seconds for the next question
    sleep(10)

with open('session.json', 'w') as f:
    json.dump(client.getSession(), f)
    
# client.logout()

