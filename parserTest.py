"""
Reddit crawler using Pushshift.io API. 
Based off code here: https://github.com/Watchful1/Sketchpad/blob/master/postDownloader.py
"""

import requests
from datetime import datetime
from dateutil import tz
import traceback
import time
import csv
import praw
import os
from dotenv import load_dotenv, find_dotenv

subreddit = "encouragement"
load_dotenv(find_dotenv())
reddit = praw.Reddit(client_id=os.environ.get("REDDIT_CLIENT_ID"),
                     client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
                     password=os.environ.get("REDDIT_PASSWORD"),
                     user_agent="testscript by Jason for CMPU365",
                     username=os.environ.get("REDDIT_USER"))
start_time = datetime.utcnow()

def downloadFromURL(filename, start=datetime.utcnow(), end=0):
    print(f"Saving comments to {filename}")
    print(start, end)

    count = 0
    outputFile = open(filename, 'w', newline='') 
    writer = csv.writer(outputFile)
    writer.writerow(["Comment", "Parent Post"])
    previous_epoch = int(start.timestamp())
    end_epoch = int(end.timestamp())
    while True:
        if previous_epoch <= end_epoch:
            break
        new_url = f"https://api.pushshift.io/reddit/comment/search?limit=1000&sort=desc&subreddit={subreddit}&before={str(previous_epoch)}"
        print("new_url: ", new_url)
        comment_json = requests.get(new_url, headers={'User-Agent': 'Comment downloader adapted from /u/Watchful1'})
        time.sleep(1)
        comment_json_data = comment_json.json()
        if 'data' not in comment_json_data:
            break
        comments = comment_json_data['data']
        if len(comments) == 0:
            break
        for comment in comments:
            time.sleep(1)
            previous_epoch = comment['created_utc'] - 1
            parentID = comment['parent_id']
            if parentID.startswith('t3'):
                try:
                    parentID = parentID[3:]
                    parentText = reddit.submission(id=parentID).selftext
                    commentText = comment['body']
                    if commentText == '[removed]' or commentText == '[deleted]':
                        continue
                    commentTextASCII = commentText.encode(encoding='ascii', errors='ignore').decode()
                    commentTextASCII = commentTextASCII.replace("\n", "")
                    if parentText != '' and parentText != '[removed]' and parentText != '[deleted]':
                        # writer.writerow([commentTextASCII, "Unavailable"])
                        # print(f"Couldn't access post's text: {reddit.submission(id=parentID).url} for comment: https://www.reddit.com{comment['permalink']}")
                        parentTextASCII = parentText.encode(encoding='ascii', errors='ignore').decode()
                        parentTextASCII = parentTextASCII.replace("\n", "")
                        writer.writerow([commentTextASCII, parentTextASCII])
                        count += 1
                    else: 
                        time.sleep(1)
                        post_url = f"https://api.pushshift.io/reddit/submission/search/?ids={parentID[3:]}"
                        post_json = requests.get(post_url)
                        post_json_data = post_json.json()
                        print("post json: ", post_json_data)
                except Exception as err:
                    # print(f"Couldn't print comment: https://www.reddit.com{comment['permalink']}")
                    print(traceback.format_exc())
        print(f"Saved {count} comments through {datetime.fromtimestamp(previous_epoch).strftime('%Y-%m-%d')}")
    print(f"Saved {count} comments")
    outputFile.close()

breakTime = datetime(2019, 5, 1, tzinfo=tz.gettz('utc'))
startofsub = datetime(2011, 8, 25, tzinfo=tz.gettz('utc'))
downloadFromURL("encouragement_topLevelComments_start_2.csv", breakTime, startofsub)

                    # parent_url = f"https://api.pushshift.io/reddit/search/submission/?ids={parentID}"
                    # parent_json = requests.get(parent_url, headers={'User-Agent': 'Post downloader adapted from /u/Watchful1'})
                    # parent_json_data = parent_json.json()
                    # parentObject = parent_json_data['data'][0]
                    # parentText = parentObject['selftext']
#1472169600