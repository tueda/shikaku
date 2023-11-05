"""Toolbox for Japanese text."""

from .loader import load_aozorabunko
from .textmodel import TextModel
from .wordcloud import WordCloud

__all__ = (
    "load_aozorabunko",
    "TextModel",
    "WordCloud",
)

__version__ = "0.0.1"
