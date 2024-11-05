import wikipediaapi
import wikipedia
import requests
from bs4 import BeautifulSoup
from utils import Metadata, metadata_path

wiki_wiki = wikipediaapi.Wikipedia("Jaseci Lab University of Michigan", "en")


def get_all_pages_in_category(category_name, language="en"):
    category = wiki_wiki.page("Category:" + category_name)
    categories = []
    pages = {}

    def fetch_pages(category_page):
        # Get articles in this category
        print(category_page.title)
        for title, member in category_page.categorymembers.items():
            if member.ns == 0:
                if title not in pages:
                    pages[title] = member
            elif member.ns == 14 and title not in categories:
                categories.append(title)
                fetch_pages(member)

    fetch_pages(category)
    return pages


def fetch_images(page: wikipediaapi.WikipediaPage):
    # Download the HTML text of the page
    return wikipedia.page(page.title).images


def extract_links(pages):
    links = {}
    for title, page in pages.items():
        links[title] = [link for link in page.links if link in pages.keys()]
    return links


# Example usage:
category_name = "Machine learning"  # Change this to your desired category
print(fetch_images(wiki_wiki.page("Blockchain")))
exit(0)
pages = get_all_pages_in_category(category_name)

# Print the titles of all related pages
print("Pages related to category:", category_name)
for title in pages.keys():
    print(title)
print("Total number of pages:", len(pages))
print(extract_links(pages))
