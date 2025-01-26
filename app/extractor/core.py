from datetime import datetime
from .constants import Site, SAVE_PATH
from .crawler import page


def extract(site: Site, url: str, name: str) -> dict:
    save_path = SAVE_PATH.format(
        site=site.value, name=name, date=datetime.now().strftime("%Y-%m-%d")
    )

    if not (html := page.load_page(url, save_path)):
        return {}

    return site.parse(html)
