"""
Research Dashboard - Detail Page

Shows full content for a single research item.
The item is selected via the `id` query parameter, e.g.:
    /Detail?id=2026-04-30_best-ups-for-nas

(This page is what shows when you click a research item from the home page.
It displays the full report, the LLM analysis, and metadata.)
"""

import pandas as pd
import streamlit as st

from lib.data import load_all_research



# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Research Detail",
    page_icon="🔍",
    layout="wide",
)



# -----------------------------------------------------------------------------
# Load data and find the requested item
# -----------------------------------------------------------------------------
df = load_all_research()

# Read the ?id=... query parameter from the URL
# st.query_params returns a dict-like object of URL parameters
research_id = st.query_params.get("id")

if research_id is None:
    st.warning("No research item selected.")
    st.page_link("app.py", label="← Back to dashboard")
    st.stop()

# Find the row matching this ID
matching_rows = df[df["id"] == research_id]

if matching_rows.empty:
    st.error(f"Research item not found: `{research_id}`")
    st.page_link("app.py", label="← Back to dashboard")
    st.stop()

# Get the single row as a dict for easier access
item = matching_rows.iloc[0].to_dict()



# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.page_link("app.py", label="← Back to dashboard")

st.title(item["title"])

# Metadata row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Date", item["created_at"][:10])
col2.metric("Category", item["category"])
col3.metric("Threads", item["total_threads"])
col4.metric("Comments", item["total_comments"])
col5.metric("Upvotes", item["total_upvotes"])

# Project tage if present
if pd.notna(item.get("project")):
    st.caption(f"🔧 Project: **{item['project']}**")



# -----------------------------------------------------------------------------
# Question
# -----------------------------------------------------------------------------
st.divider()
st.subheader("📝 Question")
st.markdown(f"> {item['question']}")



# -----------------------------------------------------------------------------
# Tabbed Content: Analysis | Report
# -----------------------------------------------------------------------------
st.divider()

tab_analysis, tab_report = st.tabs(["🇦🇮 LLM Analysis", "💬 Full Report"])

with tab_analysis:
    if item["analysis"]:
        st.markdown(item["analysis"])
    else:
        st.info("No analysis file found for this research.")
    
with tab_report:
    if item["report"]:
        st.markdown(item["report"])
    else:
        st.info("No report file found for this research.")



# -----------------------------------------------------------------------------
# Footer - Notes and Metadata
# -----------------------------------------------------------------------------
st.divider()

with st.expander("ℹ️ Metadata"):
    st.code(f"ID: {item['id']}")
    st.code(f"Folder: {item['folder_path']}")
    if item.get("notes"):
        st.write("**Notes:**")
        st.write(item["notes"])


