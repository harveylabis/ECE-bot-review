"""LOG IN AND SEND THE QUESTION, CHOICES, AND ANSWER; MAIN DRIVER PROGRAM
A program the periodically message an ECE-related questions to Facebook
group chat using 'fbchat' module.

author: pororomero
created: 7/18/2021
"""

import credentials
import json
from fbchat import Client
from fbchat.models import *
import fetch_item
from time import sleep
import tracker

# log in details
username = credentials.getEmail()
password = credentials.getPassword()
chatIDs = credentials.getChatID()
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" # old user agent works
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

# open the counter to know which number to start
id_counter = tracker.read_counter()

# get questions and answers
question_count = id_counter
items = fetch_item.get_item(str(question_count))

for item in items:
    topic = item[0]
    question = item[1]
    url = item[2]
    choices = item[3]
    key_ans = item[4]

    
    print("Topic:", topic)
    print("Sending QUESTION: ", question)
    client.send(Message(text=topic + "\n\n" + question), thread_id=chatIDs, thread_type=ThreadType.USER) # send question
    sleep(15) # wait for 15 sec before sending url if present, otherwise, choices

    # sending image url if present
    if url:
        client.send(Message(text=url), thread_id=chatIDs, thread_type=ThreadType.USER) # send question
        sleep(5) # wait for 5 sec before sending choices

    for choice in choices:
        print("Sending CHOICE:       ", choice)
        client.send(Message(text=choice), thread_id=chatIDs, thread_type=ThreadType.USER) # send choices
        sleep(1) # send choices for evey 1 second interval

    # after 15 sec for testing, send the answer key
    sleep(15)
    client.send(Message(text=key_ans), thread_id=chatIDs, thread_type=ThreadType.USER) # send key answer
    print("Sending KEY ANS:    ", key_ans)

    # wait for 5 seconds for the next question
    sleep(5)

tracker.write_counter(question_count)
print("The question was sent properly, exiting...")
    
# client.logout() - cause error, better not include

