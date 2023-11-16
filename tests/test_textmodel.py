import shikaku.textmodel


def test_preprocess_text() -> None:
    s = """\

　私は猫です。
私は犬です！鳥です
「猫だ？」
「山だ。」と言った。「谷だ。」
「川だ。」と言った。
（狼だ。）
「カレーは
飲み物」。
猿だ
"""
    r = """\
私 は 猫 です
私 は 犬 です ！
猫 だ ？
谷 だ
狼 だ
""".strip().splitlines()
    assert shikaku.textmodel._preprocess_text(s) == r


def test_generate() -> None:
    model = shikaku.textmodel.TextModel(state_size=2)
    model.fit("これはペンです。")
    assert model.generate() == "これはペンです。"
    assert model.generate(beginning="これ") == "これはペンです。"
    assert model.generate(beginning="これは") == "これはペンです。"
