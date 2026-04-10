import json
import time
import requests
from datetime import date 

# Updated May 9 2026, from day1_v8_analyze.py
# v8: removing link for each comment, makes readability a lot harder
# adding indentation code for better readability, on the report

###############################################################
### NOTE: Recommended to change 'TOPIC' variable before use ###
###############################################################

TOPIC = "add topic here"

all_content = []            # list with raw json content (comments)
formatted_comments = []     # two nested loops, one for each thread, one for each comment inside that thread
report_lines = []           # list filled with strings, one per line of the final report (for you to read through each comment)
subreddit_comments = 0      # number of reponse comments from that particular subreddit
subreddit_count = 0         # number of subreddits analyzed total (for this question)
total_comments = 0          # total number of comments analyzed

# send prompt to Ollama
def ask_llm(prompt, think=False):
    """Send a prompt to Ollama and return the response."""
    prefix = "" if think else "/no_think "
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen3:14b",
        "prompt": prefix + prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    })
    raw = response.text
    lines = raw.strip().split("\n")
    full_response = ""
    for line in lines:
        data = json.loads(line)
        if "response" in data:
            full_response += data["response"]
    return full_response

start = time.time()

# open JSON file and dump it into 'all_content'
with open(f"data/scan_{TOPIC}_{date.today()}.json", "r", encoding="utf-8") as f:
    all_content = json.load(f)
    question = all_content[0]["question"]   # question text, to give LLM more context, for better analysis


for thread in all_content:
    start1 = time.time()
    subreddit = thread["subreddit"]
    subreddit_comments = 0
    subreddit_count += 1
    sorted_thread = sorted(thread["comments"], key=lambda c: c["score"], reverse=True)
    for comment in sorted_thread:
        body = comment["body"]
        score = comment["score"]
        author = comment["author"]
        line = f"[r/{subreddit}] [score: {score}] {author}: {body}"
        subreddit_comments += 1
        formatted_comments.append(line)
    elapsed1 = time.time() - start1
    print(f"\nAnalyzed {subreddit_comments} comments in r/{subreddit} in {elapsed1:.5f} seconds.")
    total_comments = total_comments + subreddit_comments

all_comments_text = "\n\n".join(formatted_comments)



report_lines.append(f"# Reddit Comment Report - {date.today()}\n")
report_lines.append(f"**Total comments:** {total_comments} across {subreddit_count} subreddits\n")

# sort order of subreddit section returned, by highest comment upvote rank within each subreddit 
# (e.g. if most upvoted comment is 10, 55, 23, 3, 2 in each subreddit... it will return report with subreddit sections arranged 
# by most upvoted. In this case: 55, 23, 10, 3, 2)
all_content_sorted = sorted(all_content, key=lambda t: max(c["score"] for c in t["comments"]) if t["comments"] else 0, reverse=True)

# sort order 
for thread in all_content_sorted:
    subreddit = thread["subreddit"]
    url = thread["url"].replace(".json", "")
    # A lambda is an inline mini function. Same as writing `def get_score(c): return c["score"]`, but in one line.
    sorted_comments = sorted(thread["comments"], key=lambda c: c["score"], reverse=True)    # reverse=True means highest first

    report_lines.append(f"\n---\n")
    report_lines.append(f"## [r/{subreddit}]({url})")
    report_lines.append(f"**{len(sorted_comments)} comments**\n")


    for c in sorted_comments:
        score = c["score"]
        prefix = f"+{score}" if score >= 0 else str(score)
        comment_url = f"{url}comment/{c['id']}"
        indent = "  " * c.get("depth", 0)
        report_lines.append(f"{indent}- **[{prefix}]** **{c['author']}**: {c['body']}\n")
        # report_lines.append(f"  [link]{comment_url}\n")  # <-- removed this, it was making the final report much too noisy

report_text = "\n".join(report_lines)   # glues all text from `report_lines[]` into one big string (ie. the full report) 

with open(f"data/report_{TOPIC}_{date.today()}.md", "w", encoding="utf-8") as f:
    f.write(f"# Original Question\n\n{question}\n\n")
    f.write(report_text)
print(f"Report saved to data/report_{TOPIC}_{date.today()}.md")



# summarize with local LLM
print("\nAnalyzing with LLM...")
start = time.time()

prompt = f"""I posted the same question across multiple subreddits. Analyze ALL the responses and give me:

1. CONSENSUS: What do most people agree on?
2. TOP RECOMMENDATIONS: What specific products/brands/solutions were recommended most, and by how many people?
3. CONTRARIAN INSIGHTS: Any downvoted or low-score comments that actually make good points?
4. WARNINGS: What should I avoid and why?
5. ACTION ITEMS: Based on everything, what should I actually do?
6. NOTE: Only reference information that was actually stated in the comments. Do not add outside knowledge.
7. BE SPECIFIC. Count repeated ideas when possible.
8. ACTION ITEMS (Anciallary considerations): What action steps do people recommend for me to do? Maybe things I didn't consider? List them all out in an easy-to-implement manner.

Here is my question: 
{question}

Here are the responses from {subreddit_count} subreddits:

All Comments: 
{all_comments_text}

"""



# call function that sends prompt to Ollama
full_response = ask_llm(prompt)

# save analysis to file
analysis_file = f"data/analysis_{TOPIC}_{date.today()}.txt"
with open(analysis_file, "w", encoding="utf-8") as f:
    f.write(full_response)



# answers_file = f"data/analysis_{date.today()}.txt"
# with open(answers_file, "w", encoding="utf-8") as f:
#    f.write(full_response)

print(f"\n\n{'='*50}")
print("ANALYSIS")
print(f"{'='*50}")
print(full_response)
print(f"\n\nAnalysis saved to: {analysis_file}")
print(f"Full list of Reddit answers saved to: data/report_{date.today()}.md")


