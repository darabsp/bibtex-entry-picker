# bibtex-entry-picker

BibTeXのエントリを文字列に整形してクリップボードにコピーするもの

## How to use

### Install packages

パッケージ管理に[uv](https://docs.astral.sh/uv/)を使用しています。
`uv sync` を実行することでパッケージのインストールが可能です。

### Execute

`uv run main.py <bib file path> <entry key>`

`entry key` が完全一致せず、部分一致検索によってエントリが一意に特定できる場合はそれがコピーされます。
