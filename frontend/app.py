import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Add project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

# Load environment variables
load_dotenv()

from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache, InMemoryCache

# Use InMemoryCache for Streamlit Cloud, SQLiteCache for local development
if os.path.exists("data"):
    # Local environment - use persistent cache
    os.makedirs("data/llm_cache", exist_ok=True)
    set_llm_cache(SQLiteCache(database_path="data/llm_cache/langchain.db"))
else:
    # Streamlit Cloud - use in-memory cache
    set_llm_cache(InMemoryCache())

# Configure page settings
st.set_page_config(
    page_title="LLM-TextKit",
    page_icon="🚀",
)

# Define pages
home_page = st.Page("Home.py", title="首页", icon=":material/home:", default=True)

sentiment_analysis = st.Page(
    "page/sentiment_analysis.py",
    title="情感分析与标注",
    icon=":material/family_star:",
)

text_clustering = st.Page(
    "page/text_clustering.py",
    title="文本聚类分析",
    icon=":material/folder_open:",
)

ai_translation = st.Page(
    "page/ai_translation.py",
    title="智能语境翻译",
    icon=":material/translate:",
)

# Page navigation
page_dict = {
    "主页": [home_page],
    "文本处理功能": [sentiment_analysis, text_clustering, ai_translation],
}

pg = st.navigation(page_dict)
pg.run()
