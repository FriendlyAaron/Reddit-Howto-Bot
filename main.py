import praw
import os
import json
from youtubesearchpython import *
import time
from keep_alive import keep_alive

#Login 
reddit = praw.Reddit(
 client_id = os.environ ['client_id'],
  client_secret = os.environ ['client_secret'],
  username = os.environ ['username'],
  password = os.environ ['password'],
  user_agent = '<FriendlyHowToBot>'
)  


# Check if comment is valid and gets keywords
def fetch_comment(comment):
  keywords = comment.body.lower()
  if ((keywords.startswith("!how do i ") or keywords.startswith("!how to ")) and len(keywords) <= max_length and "!<" not in keywords and ">!" not in keywords):
    print (len(keywords))
    print(keywords)
    start = keywords.index("!how") + 1
    try:
      end = keywords.index("?")
      keywords = keywords[start:end]
    except:
      keywords = keywords[start:]
    print (keywords)
    video = fetch_video(keywords)
    reply(comment,video)

#Get video url
def fetch_video(keywords):
  search = SearchVideos(keywords, offset = 1, mode = "json", max_results = 1)
  r = search.result()
  res = json.loads(r)
  res1 = res['search_result']
  res2 = res1[0]
  res_fin = res2['link']
  print(res_fin)
  return res_fin

#Reply to comment
def reply(comment,video):
  comment.reply("Beep boop Im a bot and based on your comment, I see you might need some help. "+"I hope this Youtube video will help you. "+video+"\n\nCommands: !how do I, !how to")
  print ("Replied!")


keep_alive()
subreddit = reddit.subreddit("all")
max_length = 60;
def post():
  for comment in subreddit.stream.comments(skip_existing=True):
    fetch_comment(comment) 
  
while True:
  try:
    post()
    time.sleep(21600)
  except Exception as e:
    post()
    time.sleep(21600)
