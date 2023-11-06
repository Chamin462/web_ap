import streamlit as st
import requests
import textrazor
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from collections import Counter

# Set up your Google Custom Search API credentials and TextRazor API key
google_search_api_key = "AIzaSyCWj7P_c8yBHk14vp1Z1KA0JoBtqo6phtM"
google_cse_id = "13c12b8b5548447d3"
textrazor.api_key = "df186012d54042037397f5b19f31d8760ab3c6306458700ad31a8584"

# Function to fetch the top 10 google search results for a keyword using Google Custom Search API
def get_top_10_results(keyword):
    try:
        service = build("customsearch", "v1", developerKey=google_search_api_key)
        results = service.cse().list(q=keyword, cx=google_cse_id).execute()

        search_results = []
        if "items" in results:
            for item in results["items"]:
                link = item["link"]
                search_results.append(link)

            return search_results[:10]
    except Exception as e:
        print(f"Error in get_google_results: {str(e)}")
        return []

# Function to analyze entities on a webpage using TextRazor
def analyze_entities_on_page(url):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        # Initialize TextRazor client for entities extraction
        client = textrazor.TextRazor(extractors=["entities"])
        # Analyze the web content using TextRazor
        response = client.analyze(text)

        entities = set()
        for entity in response.entities():
            entities.add(entity.id)

        return entities
    except Exception as e:
        print(f"Error in analyze_entities_on_page: {str(e)}")
        return set()

# Streamlit web app
st.title("Google Search Entity Analyzer")

keyword = st.text_input("Enter a keyword to search on Google:")

if st.button("Analyze"):
    google_results = get_top_10_results(keyword)

    # List to store links to analyze
    links_to_analyze = []

    # Dictionary to store counts
    entity_counts = Counter()

    # Analyze entities for each link
    for link in google_results:
        st.write(f"Analyzing entities for {link}....")
        entities = analyze_entities_on_page(link)
        entity_counts.update(entities)
        links_to_analyze.append(link)

    # Get the top 100 common entities
    common_entities = [entity for entity, count in sorted(entity_counts.items(), key=lambda item: item[1], reverse=True)[:100]]

    # Display the top common entities
    st.write("Top 100 Common Entities:")
    for entity in common_entities:
        st.write(entity)

