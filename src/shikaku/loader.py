"""Text loaders."""

import functools
import io
import re
import urllib.request
import warnings
import zipfile


@functools.cache
def _download(url: str) -> bytes:
    """Return the file contents downloaded from the given URL.

    Parameters
    ----------
    url : str
        URL for downloading data.

    Returns
    -------
    bytes
        Downloaded data.

    """
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")

    # We need S310 here to suppress false positives.
    # See: https://github.com/astral-sh/ruff/issues/7918
    with urllib.request.urlopen(url) as f:  # noqa: S310
        return f.read()  # type: ignore[no-any-return]


def _remove_annotations(text: str) -> str:
    """Remove annotations in the text.

    Parameters
    ----------
    text : str
        Input text.

    Returns
    -------
    str
        Processed text.

    """
    # Remove the opening metadata.
    text = re.split(r"(?m)^[^\S\r\n]*\r?\n", text, maxsplit=1)[-1]
    # Remove the optional notation legend.
    text = re.split(r"(?m)^\-{5,}", text, maxsplit=2)[-1]
    # Remove the footer.
    text = re.split(r"(?m)^(?:底本：|［＃本文終わり］)", text, maxsplit=1)[0]
    # Remove ruby annotations.
    text = re.sub("｜", "", text)
    text = re.sub("《.+?》", "", text)
    # Remove transcriber annotations.
    text = re.sub("［＃.+?］", "", text)
    return text.strip()


class AozoraBunkoFileError(ValueError):
    """Error raised for unexpected format in files on Aozora Bunko."""


class AozoraBunkoFileWarning(Warning):
    """Warning raised for unexpected format in files on Aozora Bunko."""


def load_aozorabunko(author_id: int, work_id: int, *, raw: bool = False) -> str:
    """Return text downloaded from Aozora Bunko.

    Parameters
    ----------
    author_id : int
        Author ID.
    work_id : int
        Work ID.
    raw : bool, default False
        Whether it returns a raw text or not.

    Returns
    -------
    str
        Downloaded text.

    Example
    -------
    >>> load_aozorabunko(35, 1567)  # doctest: +SKIP
    ... # author_id: 35, work_id: 1567 => "Run, Melos!"

    """
    # Use the plain-text mirror for works commonly used in examples.
    mirror_url = _get_text_mirror(author_id, work_id)
    if mirror_url:
        text = _download(mirror_url).decode("shift-jis")
    else:
        text = _extract_from_zip(author_id, work_id)

    if not raw:
        text = _remove_annotations(text)

    return text


def _extract_from_zip(
    author_id: int,
    work_id: int,
    prefix: str = "https://www.aozora.gr.jp",
) -> str:
    # Download the corresponding library card.
    card_file = f"{author_id:0=6}/card{work_id}.html"
    card = _download(f"{prefix}/cards/{card_file}").decode("utf-8")

    # Search for the ZIP file with ruby text from the library card.
    m = re.search(r"\d+_ruby_\d+\.zip", card)
    if not m:
        # Fallback to the ZIP file without ruby text.
        m = re.search(r"\d+_txt_\d+\.zip", card)
        if not m:
            raise AozoraBunkoFileError(f"ZIP file not detected in {card_file}")
    zipname = m.group(0)

    # Download the ZIP file.
    zipdata = zipfile.ZipFile(
        io.BytesIO(_download(f"{prefix}/cards/{author_id:0=6}/files/{zipname}")),
    )

    # Find text files in the ZIP file.
    text_filenames = [s for s in zipdata.namelist() if s.lower().endswith(".txt")]
    if not text_filenames:
        raise AozoraBunkoFileError(f"text file not found in {zipname}")
    if len(text_filenames) >= 2:
        warnings.warn(
            f"more than one text files found: {text_filenames}. Take the first one",
            AozoraBunkoFileWarning,
            stacklevel=2,
        )
    filename = text_filenames[0]

    # Extract text from the ZIP file.
    return zipdata.read(filename).decode("shift-jis")


def _get_text_mirror(author_id: int, work_id: int) -> str | None:
    key = (author_id, work_id)
    if key in _aozorabunko_text_cards:
        return (
            f"{_aozorabunko_text_prefix}/{author_id:0=6}/files/"
            f"{_aozorabunko_text_cards[key]}"
        )
    return None


_aozorabunko_text_prefix = "https://raw.githubusercontent.com/aozorahack/aozorabunko_text/refs/heads/master/cards"

_aozorabunko_text_cards = {
    # Run, Melos!
    (35, 1567): "1567_ruby_4948/1567_ruby_4948.txt",
    # Lemon
    (74, 424): "424_ruby_19825/424_ruby_19825.txt",
    # The Wild Pear
    (81, 472): "472_ruby_654/472_ruby_654.txt",
    # The Restaurant of Many Orders
    (81, 1927): "1927_ruby_17835/1927_ruby_17835.txt",
    # Night on the Galactic Railroad
    (81, 43737): "43737_ruby_19028/43737_ruby_19028.txt",
    # The Moon over the Mountain
    (119, 623): "623_ruby_18352/623_ruby_18352.txt",
    # Gon, the Little Fox
    (121, 628): "628_ruby_649/628_ruby_649.txt",
    # Kokoro  # cspell:disable-line  # noqa: ERA001
    (148, 773): "773_ruby_5968/773_ruby_5968.txt",
    # I Am a Cat
    (148, 789): "789_ruby_5639/789_ruby_5639.txt",
    # Rashōmon  # cspell:disable-line  # noqa: ERA001
    (879, 127): "127_ruby_150/127_ruby_150.txt",
}
