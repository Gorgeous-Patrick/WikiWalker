import json
from utils import PageInfo
def read_page_text(title: str):
    with open(f"data/cache/{title.replace('/', '_')}.json", "r") as file :
        parsed = json.load(file)
        page = PageInfo(**parsed)
        return page.text