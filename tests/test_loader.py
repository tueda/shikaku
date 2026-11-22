import io
import zipfile
from collections.abc import Iterator
from unittest.mock import Mock, call

import pytest

import shikaku.loader


@pytest.fixture
def mock_urlopen(monkeypatch: pytest.MonkeyPatch) -> Iterator[Mock]:
    shikaku.loader._download.cache_clear()
    mock = Mock(side_effect=AssertionError("Unexpected download"))
    monkeypatch.setattr(shikaku.loader.urllib.request, "urlopen", mock)
    try:
        yield mock
    finally:
        shikaku.loader._download.cache_clear()


def _zip_response(files: dict[str, bytes]) -> io.BytesIO:
    response = io.BytesIO()
    with zipfile.ZipFile(response, "w") as archive:
        for name, contents in files.items():
            archive.writestr(name, contents)
    response.seek(0)
    return response


def test_download_rejects_unsupported_scheme(mock_urlopen: Mock) -> None:
    with pytest.raises(ValueError, match="URL must start with"):
        shikaku.loader._download("file:///tmp/test.txt")


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


def test_load_aozorabunko_from_zip(mock_urlopen: Mock) -> None:
    card_html = b'<a href="./files/999999_ruby_9999.zip">999999_ruby_9999.zip</a>.zip'
    text = "走れメロス"
    mock_urlopen.side_effect = [
        io.BytesIO(card_html),
        _zip_response(
            {"readme.md": b"Ignore this file", "work.txt": text.encode("shift-jis")}
        ),
    ]
    assert shikaku.loader.load_aozorabunko(999999, 9999, raw=True) == text
    assert shikaku.loader.load_aozorabunko(999999, 9999, raw=True) == text
    assert mock_urlopen.call_args_list == [
        call("https://www.aozora.gr.jp/cards/999999/card9999.html"),
        call("https://www.aozora.gr.jp/cards/999999/files/999999_ruby_9999.zip"),
    ]


def test_load_aozorabunko_from_zip_without_ruby(mock_urlopen: Mock) -> None:
    # See: https://github.com/tueda/shikaku/issues/2
    card_html = b'<a href="./files/999999_txt_9999.zip">999999_txt_9999.zip</a>.zip'
    text = "相対性理論"
    mock_urlopen.side_effect = [
        io.BytesIO(card_html),
        _zip_response(
            {"readme.md": b"Ignore this file", "work.txt": text.encode("shift-jis")}
        ),
    ]
    assert shikaku.loader.load_aozorabunko(999999, 9999, raw=True) == text
    assert shikaku.loader.load_aozorabunko(999999, 9999, raw=True) == text
    assert mock_urlopen.call_args_list == [
        call("https://www.aozora.gr.jp/cards/999999/card9999.html"),
        call("https://www.aozora.gr.jp/cards/999999/files/999999_txt_9999.zip"),
    ]


def test_load_aozorabunko_from_mirror(mock_urlopen: Mock) -> None:
    text = "走れメロス"
    mock_urlopen.side_effect = [io.BytesIO(text.encode("shift-jis"))]
    assert shikaku.loader.load_aozorabunko(35, 1567, raw=True) == text
    assert shikaku.loader.load_aozorabunko(35, 1567, raw=True) == text
    mock_urlopen.assert_called_once_with(
        "https://raw.githubusercontent.com/aozorahack/aozorabunko_text/"
        "refs/heads/master/cards/000035/files/1567_ruby_4948/1567_ruby_4948.txt",
    )
