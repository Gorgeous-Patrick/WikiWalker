import wikipediaapi
import wikipedia
import json
import requests
from bs4 import BeautifulSoup
from utils import cache_path, PageInfo, Metadata

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
                # If cache does not exist, fetch the page
                if not (cache_path / f"{title.replace('/', '_')}.json").exists():
                    # Fetch the page
                    print("TITLE",member.title)
                    text = member.text
                    links = [link.title() for link in member.links]
                    images = fetch_images(member)
                    print(links)
                    page = PageInfo(title=title, text=text, links=links, images=images)
                    with open(cache_path / f"{title.replace('/', '_')}.json", "w") as file:
                        file.write(page.model_dump_json())


                
            elif member.ns == 14 and title not in categories:
                categories.append(title)
                fetch_pages(member)

    fetch_pages(category)
    return pages


def fetch_images(page: wikipediaapi.WikipediaPage):
    # Download the HTML text of the page
    bs = BeautifulSoup(requests.get(page.fullurl).text, "html.parser")
    images = []
    # Find all image tags
    for img in bs.find_all("img"):
        # Get the image URL
        img_url = img["src"]
        # Check if the image URL is a valid image
        if img_url.startswith("//upload.wikimedia.org"):
            images.append("https:" + img_url)
    return images


def extract_links(pages):
    links = {}
    for title, page in pages.items():
        links[title] = [link for link in page.links if link in pages.keys()]
    return links


# Example usage:
# category_name = "Machine learning"  # Change this to your desired category
# pages = get_all_pages_in_category(category_name)

# # Print the titles of all related pages
# print("Pages related to category:", category_name)
# for title in pages.keys():
#     print(title)
# print("Total number of pages:", len(pages))
