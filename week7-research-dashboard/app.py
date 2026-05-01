"""
Research Dashboard - Home Page

Lists all research items, with filtering and sorting in the sidebar.
Clicking a research itme naviates to the detail page.
"""

import pandas as pd
import streamlit as st

from lib.config import CATEGORIES, SORT_OPTIONS
from lib.data import load_all_research

# v1 - 2026-05-01
#
# df = DataFrame from load_all_research()


# ------------------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------------------
# st.set_page_config must be the first Streamlit command. It sets browser
# tab title, layout width, and other top-level settings.
st.set_page_config(
    page_title="Research Dashboard", 
    page_icon="🔍",
    layout="wide",
)



# ------------------------------------------------------------------------
# Load Data
# ------------------------------------------------------------------------
df = load_all_research()

if df.empty:
    st.error("No research items found. Check that RESEARCH_PATH in lib/config.py points to a valid folder.")
    st.stop()



# ------------------------------------------------------------------------
# Sidebar - Filters and Sorting
# ------------------------------------------------------------------------
with st.sidebar:
    st.header("Filters")

    # Category filter - multiselect so the user can pick zero or more
    # If empty, show all categories
    selected_categories = st.multiselect(
        "Category", 
        options=CATEGORIES,
        default=[],
        help="Leave empty to show all categories",
    )

    # Project Filter - Auto-discover unique project values from the data
    # Drop NaN/None values, then sort alphabetically
    available_projects = sorted([p for p in df["project"].dropna().unique()])
    selected_projects = st.multiselect(
        "Project",
        options=available_projects,
        default=[],
        help="Leave empty to show all projects (including unassigned)",
    )

    # Free-text search across title and question
    search_query = st.text_input(
        "Search",
        value="",
        help="Searches title and question text",
    )

    st.divider()
    st.header("Sort")

    # Sort Dropdown - show labels, get back the field name
    # SORT_OPTIONS is a list of (label, field) tuples form config.py
    sort_label = st.selectbox(
        "Sort by",
        options=[label for label, field in SORT_OPTIONS],
        index=0,
    )
    # Look up the field name that matches the chosen label
    sort_field = next(field for label, field in SORT_OPTIONS if label == sort_label)



# ------------------------------------------------------------------------
# Apply Filters and Sorting
# ------------------------------------------------------------------------
filtered = df.copy()            # `filtered` is a separate copy of the original DataFrame `df` we get from load_all_research()
                                #       - This is so we apply filters/sorting to `filters` and not the original DataFrame `df`

# Filter by category if any selected
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]

# Filter by project if any selected
if selected_projects:
    filtered = filtered[filtered["project"].isin(selected_projects)]

# Filter by search query - case-insensitive substring match
if search_query:
    query_lower = search_query.lower()
    title_match = filtered["title"].str.lower().str.contains(query_lower, na=False)
    question_match = filtered["question"].str.lower().str.contains(query_lower, na=False)
    filtered = filtered[title_match | question_match]

# Apply Sort
# Note: 'created_at_asc' is a special "ascending" variant of `created_at`
if sort_field == "created_at_asc":
    filtered == filtered.sort_values("created_at", ascending=True)
elif sort_field == "title":
    filtered = filtered.sort_values("title", ascending=True)
else:
    # All other sort fields default to descending (newest/highest first)
    filtered = filtered.sort_values(sort_field, ascending=False, na_position="last")



# ------------------------------------------------------------------------
# Main Area - Header
# ------------------------------------------------------------------------
st.title("🔍 Research Dashboard")
st.caption(f"Showing {len(filtered)} of {len(df)} research items")



# ------------------------------------------------------------------------
# Main Area - Research List, grouped by category
# ------------------------------------------------------------------------
if filtered.empty:
    st.info("No research items match the current filters.")
else:
    # Group by category for display
    # df.groupby preserves the order from the parent DataFrame, which is
    # already sorted by our chosen sort field
    for category, group in filtered.groupby("category", sort=False):
        st.subheader(f"{category} ({len(group)})")

        for _, row in group.iterrows():         # the underscore `_` in Python means "I know this value exists, but I don't care about it". So we're not writing out `for index, row in group.iterrows():`
            # Each row gets a container with the title as a clickable link
            # and metadata below
            with st.container(border=True):
                # Title as a link to the detail page
                # st.page_link navigates to anothe rpage, passing query params
                st.page_link(
                    page=f"pages/1_Detail.py",
                    label=f"**{row['title']}**"
                )

                # Metadata row using columns for layout
                col1, col2, col3, col4 = st.columns(4)
                col1.caption(f"📅 {row['created_at'][:10]}")
                col2.caption(f"💬 {row['total_comments']} comments  (🧵 {row['total_threads']} threads)")
                col3.caption(f"⬆️ {row['total_upvotes']} upvotes")
                if pd.notna(row.get("project")):
                    col4.caption(f"🔧 {row['project']}")
                else:
                    col4.caption("—")
                
                # Show the ID for now so we can verify naviation works
                st.caption(f"ID: `{row['id']}`")



