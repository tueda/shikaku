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
私は「犬だ。いや、猫だ」と言った。牛だった。
牛を球と近似する。私は「それだ。違う」と言った。直方体だからだ。
その「成功」は失敗だった。
"""
    r = """\
私 は 猫 です
私 は 犬 です ！
猫 だ ？
谷 だ
狼 だ
牛 だっ た
牛 を 球 と 近似 する
直方 体 だ から だ
その 「 成功 」 は 失敗 だっ た
""".strip().splitlines()
    assert shikaku.textmodel._preprocess_text(s) == r
