# bibtex-entry-picker

BibTeXのエントリを文字列に整形してクリップボードにコピーするもの

## How to use

### Install packages

パッケージ管理に[uv](https://docs.astral.sh/uv/)を使用しています。
`uv sync` を実行することでパッケージのインストールが可能です。

### Execute

`uv run main.py <bib> <key>`

`bib` の入力に応じて下記のように検索が行われます。

- `bib` にパスを入力した場合 (e.g. `../bibtex/biblio.bib`)
  - 指定されたパスがbibファイルである場合は参照します
  - 環境変数 (`BIBINPUTS`) が指すディレクトリは検索しません
- `bib` にファイル名のみを入力した場合 (e.g. `biblio.bib`, `biblio`)
  - 現在のディレクトリにファイルがある場合は参照します
  - 現在のディレクトリにファイルがない場合、環境変数 (`BIBINPUTS`) が指すディレクトリを検索します
    (サブディレクトリは検索されません)

`key` が完全一致せず、部分一致検索によってエントリが一意に特定できる場合はそれがコピーされます。
