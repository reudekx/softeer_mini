from app.extractor import fotmob_extractor

URL = "https://www.fotmob.com/ko/players/212867/heung-min-son"
SAVE_PATH = "data/{site}/html/{name}-{date}.html"


if __name__ == "__main__":
    fotmob_extractor.extract(URL, SAVE_PATH)