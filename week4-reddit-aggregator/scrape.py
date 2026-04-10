import requests
import json
from datetime import date
import os
import random
import time

# Updated May 9 2026, from day1_v6_multipleurls.py

#################################################################################
### NOTE: Recommended to change 'TOPIC' and 'User-Agent' variables before use ###
#################################################################################


TOPIC = "add topic here"

start = time.time()

headers = {
        "User-Agent": "python:reddit-aggregator:v1.0 (by u/(add a username here))"  # adding this username snippet circumvented a limit Reddit was imposing on us
    }

# parse urls.txt file to obtain individual URLs from a list
# (each URL is a post that contains Reddit comments we want to extract)
with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]
    

# return dictionaries instead of just strings (for all replies to the post, including children)
# (including vote score, to find contrarian opinions (ie. downvotes))
def extract_comments(comments):
    results = []

    for c in comments:
        if c["kind"] != "t1":   # if this is NOT a comment --> skip it  (t1 = comment)
            continue

        # filter out deleted comments. This reduces noise sent to LLM, making analysis reponse faster + higher quality
        if c["data"]["author"] in ("[deleted]", "[removed]") \
            or c["data"]["body"] in ("[deleted]", "[removed]"):
                continue

        results.append({
            "body": c["data"]["body"],
            "score": c["data"]["score"],
            "author": c["data"]["author"],
            "id": c["data"]["id"],
            "depth": c["data"]["depth"]
        })

        replies = c["data"]["replies"]
        if replies:
            results += extract_comments(replies["data"]["children"])

       
    return results


all_data = []

# main program
for url in urls:
    
    if not url.endswith(".json"):           
        url = url.rstrip("/") + "/.json"

    res = requests.get(url, headers=headers)

    print(res.status_code)

    if res.status_code != 200:
        print("Blocked. Response:")
        print(res.text[:300])
        continue

    try:
        data = res.json()
    except requests.exceptions.JSONDecodeError:
        print("Response wasn't valid JSON")
        print(res.text[:300])
        continue

    # print title once
    print(f"\n{'='*50}")
    print(data[0]["data"]["children"][0]["data"]["title"])
    print(f"\n{'='*50}")

    
    # get all comments (including replies)
    all_comments = extract_comments(data[1]["data"]["children"])
    print("\nTOTAL COMMENTS:", len(all_comments))

    all_data.append({
        "url": url,
        "title": data[0]["data"]["children"][0]["data"]["title"],
        "subreddit": data[0]["data"]["children"][0]["data"]["subreddit"],
        "question": data[0]["data"]["children"][0]["data"]["selftext"], # get original question text (gives more context to LLM as to what we're looking for / what problem we're trying to solve)
        "comments": all_comments
    })

    for comment in all_comments:
        print(f"\n[score: {comment['score']}] {comment['author']} (depth {comment['depth']})")
        print(comment["body"])

    time.sleep(random.uniform(2, 9.9))  # randomize time between accessing each url, so as not to get flagged or rate limited

filename = f"data/scan_{TOPIC}_{date.today()}.json"
os.makedirs("data", exist_ok=True)
with open(filename, "w") as f:
    json.dump(all_data, f, indent=2)
elapsed = time.time() - start
print(f"\nSaved {len(all_data)} threads to {filename} in {elapsed:.5f} seconds.")