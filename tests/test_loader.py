import shikaku.loader


def test_remove_annotations() -> None:
    s1 = """\
題名
著者名

-----
【テキスト中に現れる記号について】

-----
［＃３字下げ］今日は昨日の｜明日《あした》です。

底本：「書籍名」
底本の親本：「書籍名」
"""
    s2 = """今日は昨日の明日です。"""
    assert shikaku.loader._remove_annotations(s1) == s2
