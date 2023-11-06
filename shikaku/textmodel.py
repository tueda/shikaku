"""Markov chain model."""

import random
import re
from typing import Any, Optional

import igraph as ig
import markovify
import matplotlib.axes
import matplotlib.pyplot as plt
import MeCab
from markovify.chain import BEGIN, END


class TextModel:
    """Text generation model by Markov chain."""

    def __init__(self, state_size: int = 2) -> None:
        """
        Construct a text generation model.

        Parameters
        ----------
        state_size : int, default 2
            Markov chain state size.

        """
        self._state_size = state_size
        self._model: Optional[markovify.Text] = None
        self._compiled_model: Optional[markovify.Text] = None

    def fit(self, text: str) -> None:
        """
        Train the model.

        Parameters
        ----------
        text : str
            Text for training.

        """
        # Normalize sentence endings.
        text = re.sub("[！？。]", r"\g<0>.", text)
        # Split the text into words.
        tagger = MeCab.Tagger("-Owakati")
        text = tagger.parse(text)

        # Build a model.
        model = markovify.Text(
            text.split("."), state_size=self._state_size, well_formed=False
        )

        self._model = model
        self._compiled_model = None

    def generate(
        self,
        *,
        beginning: Optional[str] = None,
        strict: Optional[bool] = None,
        tries: Optional[int] = None,
        min_words: Optional[int] = None,
        max_words: Optional[int] = None,
    ) -> Optional[str]:
        """
        Generate a sentence.

        Parameters
        ----------
        beginning : str, optional
            Beginning word.
        strict : bool, optional
            Whether to strictly use the beginning word or not.
        tries : int, optional
            Number of tries to generate a valid sentence.
        min_words : int, optional
            Minimum number of words.
        max_words : int, optional
            Maximum number of words.

        Returns
        -------
        str or None
            Generated sentence.

        """
        if self._model is None:
            raise ValueError("model is not yet trained")

        if self._compiled_model is None:
            self._compiled_model = self._model.compile()
            # Monkey patch to generate Japanese sentences.
            self._compiled_model.word_join = lambda words: "".join(words)

        args: dict[str, Any] = {}
        if beginning is not None:
            args["beginning"] = beginning
        if strict is not None:
            args["strict"] = strict
        if tries is not None:
            args["tries"] = tries
        if min_words is not None:
            args["min_words"] = min_words
        if max_words is not None:
            args["max_words"] = max_words

        m = self._compiled_model
        if beginning is None:
            s = m.make_sentence(**args)
        else:
            s = m.make_sentence_with_start(**args)
        return s  # type: ignore[no-any-return]

    def plot(
        self,
        *,
        width: Optional[float] = None,
        height: Optional[float] = None,
        dpi: Optional[int] = None,
        layout: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> matplotlib.axes.Axes:
        """
        Plot the model.

        Parameters
        ----------
        width: float, optional
            Width of the figure.
        height: float, optional
            Height of the figure.
        dpi: int, optional
            Resolution of the figure.
        layout: str, optional
            Layout of the graph.
        seed : int, optional
            Random seed.

        Returns
        -------
        matplotlib.axes.Axes :
            Matplotlib axes containing the plot.

        """
        if self._model is None:
            raise ValueError("model is not yet trained")

        if width is None:
            width = 10
        if height is None:
            height = width

        if seed is not None:
            random.seed(seed)

        m = self._model.chain.model
        n = self._model.state_size
        beginning_state = (BEGIN,) * n
        endding_state = (END,)

        vertices: dict[tuple[str, ...], int] = {}
        edges = []
        weights = []

        def get_state_name(state: tuple[str, ...]) -> str:
            if all(x == BEGIN for x in state):
                return "BEGIN"
            if END in state:
                return "END"
            s = list(state)
            while s[0] == BEGIN:
                del s[0]
            return ",".join(s)

        def traverse(state: tuple[str, ...]) -> None:
            if state in vertices:
                return
            vertices[state] = len(vertices)

            if state not in m:
                return

            total_weight = sum(m[state].values())

            for next_word, weight in m[state].items():
                if next_word == END:
                    next_state = endding_state
                else:
                    next_state = state[1:] + (next_word,)  # type: ignore[assignment]
                traverse(next_state)
                edges.append((vertices[state], vertices[next_state]))
                weights.append(weight / total_weight)

        traverse(beginning_state)

        _, ax = plt.subplots(figsize=(width, height), dpi=dpi)

        g = ig.Graph(len(vertices), edges, directed=True)
        ig.plot(
            g,
            target=ax,
            layout=layout,
            vertex_label=[get_state_name(x) for x in vertices],
            vertex_color="#f99",
            vertex_frame_color="#999",
            edge_label=[f"{x:.02f}" for x in weights],
            edge_color="#999",
            edge_label_color="#33f",
            edge_width=0.5,
            edge_arrow_width=10,
            edge_arrow_size=10,
            edge_align_label=True,
        )

        return ax
