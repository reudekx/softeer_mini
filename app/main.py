from app.extractor import fotmob_extractor
import pandas as pd


URL = "https://www.fotmob.com/ko/players/212867/heung-min-son"
SAVE_PATH = "data/{site}/html/{name}_{date}.html"


if __name__ == "__main__":

    name = "heung-min-son"
    site = "fotmob"

    data = fotmob_extractor.extract(URL, site, name, SAVE_PATH)

    print(data)