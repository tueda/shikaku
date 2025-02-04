# Changelog


<a name="0.2.3"></a>
## [0.2.3] (2024-10-13)

- Support Python 3.12.

### Changed

- Replace [`japanize-matplotlib`](https://github.com/uehara1414/japanize-matplotlib)
  with [`matplotlib-fontja`](https://github.com/ciffelia/matplotlib-fontja).
  The former does not work with Python 3.12, while the latter is a fork that addresses this issue.
  ([42f35ba](https://github.com/tueda/shikaku/commit/42f35bab177c6bde637e7d7fee351a15dc4d78b3))


<a name="0.2.2"></a>
## [0.2.2] (2023-12-02)

### Changed

- `load_aozorabunko()` raises `AozoraBunkoFileError` instead of `ValueError`
  when no ZIP file name is found in card files.
  ([a9f3848](https://github.com/tueda/shikaku/commit/a9f3848ed4da2e1ed02cb6b174d70e214fa530d5))

### Fixed

- `load_aozorabunko()` failed to load book files with images attached.
  ([#3](https://github.com/tueda/shikaku/issues/3))


<a name="0.2.1"></a>
## [0.2.1] (2023-11-29)

### Fixed

- `load_aozorabunko()` did not work for files without ruby text.
  ([#2](https://github.com/tueda/shikaku/issues/2))
- `beginning` option of `TextModel.generate()` did not work with more than one words.
  ([e3b9b50](https://github.com/tueda/shikaku/commit/e3b9b505397cda189c3ad557960179d58ba09c43))


<a name="0.2.0"></a>
## [0.2.0] (2023-11-07)

### BREAKING CHANGE

- Some options in `TextModel.plot()` are changed to replace dependent libraries.
  ([1309620](https://github.com/tueda/shikaku/commit/1309620b3f1e9048e086eb30a31d1161a5f8cab1))

### Changed

- Switch from [NetworkX](https://networkx.org/) to [igraph](https://python.igraph.org/).
  ([1309620](https://github.com/tueda/shikaku/commit/1309620b3f1e9048e086eb30a31d1161a5f8cab1))

### Added

- Improve text handling in `TextModel`.
  ([5a25ee3](https://github.com/tueda/shikaku/commit/5a25ee333bcc9af572a50a04b903e2acc0aaced2))
- Add `raw` option to `load_aozorabunko()`.
  ([2f6d682](https://github.com/tueda/shikaku/commit/2f6d682ebcc84e5976380ad59a8ea9c24f4ae944))
- Add `seed` option to `TextModel.generate()` and `WordCloud.generate()`.
  ([162029a](https://github.com/tueda/shikaku/commit/162029a8fe62ebf7d8b43afbfdf53ccf5ad55355))

### Fixed

- `KeyError` on some bad characters.
  ([648fc62](https://github.com/tueda/shikaku/commit/648fc626de1edf8c2013b0ab728d6465dc46afef))


<a name="0.1.0"></a>
## 0.1.0 (2023-11-05)

- First release.


[0.2.3]: https://github.com/tueda/shikaku/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/tueda/shikaku/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/tueda/shikaku/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/tueda/shikaku/compare/0.1.0.post1...0.2.0
