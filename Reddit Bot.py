import praw
import os
import json
from youtubesearchpython import *
import time

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
  if ("!how do i " in  comment.body.lower() or "!how to " in  comment.body.lower()):
    print (comment.body)
    keywords = comment.body.lower()
    start = keywords.index("!how") + 1
    try:
      end = keywords.index("?")
      keywords = keywords[start:end]
    except Exception as e:
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
  rep=comment.reply("Beep boop Im a bot and based on your comment, I see you might need some help. "+"I hope this Youtube video will help you. "+video+" \n\nWas I able to help?| Downvote to remove comment| Commands: !how do I, !how to")
  print ("Replied!")
  for i in range (8):
    time.sleep(3600)
    if rep.score < 0:
      rep.delete()
      print ("deleted")
    else:
      print ("Not deleted")
  

  
    
    

subreddit = reddit.subreddit("all")

def post():
  for comment in subreddit.stream.comments(skip_existing=True):
    fetch_comment(comment) 
  
while True:
  try:
    post()
  except Exception as e:
    post()
 
