# bibtex-entry-picker

BibTeXのエントリを文字列に整形してクリップボードにコピーするもの

## How to use

### Installation

```bash
pip install git+https://github.com/darabsp/bibtex-entry-picker.git
```

#### to develop

パッケージ管理に[uv](https://docs.astral.sh/uv/)を使用しています。
uvのインストール方法については<https://docs.astral.sh/uv/getting-started/installation/>を参照してください。

```bash
git clone https://github.com/darabsp/bibtex-entry-picker.git
cd bibtex-entry-picker
uv sync
```

### Execute

```bash
bibtex-entry-picker <bib> <key>
bibpick <bib> <key>
```

`bib` の入力に応じて下記のように検索が行われます。

- `bib` にパスを入力した場合 (e.g. `../bibtex/biblio.bib`)
  - 指定されたパスがbibファイルである場合は参照します
  - 環境変数 (`BIBINPUTS`) が指すディレクトリは検索しません
- `bib` にファイル名のみを入力した場合 (e.g. `biblio.bib`, `biblio`)
  - 現在のディレクトリにファイルがある場合は参照します
  - 現在のディレクトリにファイルがない場合、環境変数 (`BIBINPUTS`) が指すディレクトリを検索します
    (サブディレクトリは検索されません)

`key` が完全一致せず、部分一致検索によってエントリが一意に特定できる場合はそれがコピーされます。
