import shikaku.utils


def test_either() -> None:
    def test(a: list[str], b: str) -> None:
        assert shikaku.utils.either(a).pattern == b

    test(["a"], "a")
    test(["a", "b", "c"], "[abc]")
    test(["ad", "bd", "cd"], "[abc]d")
    test(["ab", "ac", "ad"], "a[bcd]")
    test(["ac", "ad", "bc", "bd"], "[ab][cd]")
    test(["abc", "ad"], "a(?:bc|d)")


def test_katakana_to_vowels() -> None:
    def test(a: str, b: str) -> None:
        assert shikaku.utils.katakana_to_vowels(a) == b

    test("シークヮーサー", "イーアーアー")
    test("シミュレーション", "イウエーオン")
    test("ヱヴァンゲリヲン", "エアンエイオン")
    test("デュアルディスプレイ", "ウアウイウウエイ")
    test("ピョートル・チャイコフスキィ", "オーオウ・アイオウウイイ")
    test("ヴォルフガング・サヴァリッシュ", "オウウアンウ・アアイッウ")


def test_count_mora_in_katakana() -> None:
    def test(a: str, b: int) -> None:
        assert shikaku.utils.count_mora_in_katakana(a) == b

    test("シークヮーサー", 6)
    test("シミュレーション", 6)
    test("ヱヴァンゲリヲン", 7)
    test("デュアルディスプレイ", 8)
    test("ピョートル・チャイコフスキィ", 4 + 7)
    test("ヴォルフガング・サヴァリッシュ", 6 + 5)


def test_parse() -> None:
    a = shikaku.utils.parse("こおりつけ！")
    assert len(a) == 2
    assert a[0].surface == "こおりつけ"
    assert a[0].vowels == "オーイウエ"
    assert a[1].pos2 == "句点"

    a = shikaku.utils.parse("吾輩は猫である。")
    assert len(a) == 6
    assert a[1].surface == "は"
    assert len(a[1].aConType.split(",")) == 3
    assert a[1].vowels == "ア"

    a = shikaku.utils.parse("Ｃｒｅａｔｉｖｅ　Ｃｏｍｍｏｎｓ")
    assert len(a) == 3
    assert a[0].surface == "Ｃｒｅａｔｉｖｅ"
    assert a[0].mora == 0  # current limitation
    assert a[1].pos1 == "空白"
