from datetime import datetime
from app.constants import Site, SAVE_PATH
from . import page_crawler


def extract(site: Site, url: str, name: str) -> dict:
    save_path = SAVE_PATH.format(
        site=site.value, name=name, date=datetime.now().strftime("%Y-%m-%d")
    )

    if not (html := page_crawler.load_page(url, save_path)):
        return {}

    return site.parse(html)
