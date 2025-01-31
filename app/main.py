import app.core.extractor


def test_son_heung_min():
    site = extractor.Site.FOTMOB
    url = "https://www.fotmob.com/ko/players/212867/heung-min-son"
    name = "son-heung-min"

    fotmob_data = extractor.extract(site, url, name)

    site = extractor.Site.FBREF
    url = "https://fbref.com/en/players/92e7e919/Son-Heung-min"
    name = "son-heung-min"

    fbref_data = extractor.extract(site, url, name)

    print(fotmob_data)

    print(fbref_data)


def test_kim_min_jae():
    site = extractor.Site.FOTMOB
    url = "https://www.fotmob.com/ko/players/828159/min-jae-kim"
    name = "kim-min-jae"

    fotmob_data = extractor.extract(site, url, name)

    site = extractor.Site.FBREF
    url = "https://fbref.com/en/players/e0f8151c/Kim-Min-jae"
    name = "kim-min-jae"

    fbref_data = extractor.extract(site, url, name)

    print(fotmob_data)

    print(fbref_data)


def test_emile_smith_rowe():
    site = extractor.Site.FOTMOB
    url = "https://www.fotmob.com/ko/players/889534/emile-smith-rowe"
    name = "emile-smith-rowe"

    fotmob_data = extractor.extract(site, url, name)

    site = extractor.Site.FBREF
    url = "https://fbref.com/en/players/17695062/Emile-Smith-Rowe"
    name = "emile-smith-rowe"

    fbref_data = extractor.extract(site, url, name)

    print(fotmob_data)

    print(fbref_data)

if __name__ == "__main__":

    # test_kim_min_jae()

    # test_son_heung_min()

    test_emile_smith_rowe()