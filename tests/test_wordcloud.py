import shikaku.wordcloud


def test_get_words() -> None:
    assert shikaku.wordcloud._get_words("すもももももももものうち") == "すもも もも もも うち"
