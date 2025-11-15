from os import environ, pathsep, sep
from pathlib import Path
from pybtex.database import Entry

BIB_SUFFIX = '.bib'

def _partial_file_search(query: Path, directories: list[Path]) -> Path | None:
  matches = []
  for directory in directories:
    matches.extend(directory.glob(f'*{query.stem}*{BIB_SUFFIX}'))
  if len(matches) == 1:
    return matches[0]

def _search_file_by_path(path: Path) -> Path | None:
  return path.absolute() if path.is_file() else None

def _search_file_in_current_directory(name: Path, partial_search: bool) -> Path | None:
  if partial_search:
    return _partial_file_search(name, [Path.cwd()])
  else:
    return name if name.is_file() else None

def _search_file_in_bibinputs(name: Path, partial_search: bool) -> Path | None:
  bibinputs = environ.get('BIBINPUTS')
  if bibinputs is None:
    return None

  directories = [Path(directory) for directory in bibinputs.split(pathsep) if Path(directory).is_dir()]
  if directories == []:
    return None

  if partial_search:
    return _partial_file_search(name, directories)
  else:
    for directory in directories:
      path = directory.joinpath(name)
      if path.is_file():
        return path

# .bibファイルを探してそのpathを返す
# パスが入力された場合 (e.g. ../bibtex/biblio.bib): 指定されたパスのみ検索, 環境変数の検索は行わない
# ファイル名のみが入力された場合 (e.g. biblio.bib, biblio): カレントディレクトリと環境変数を検索
def search_bib_file(query: str) -> Path:
  path = Path(query).with_suffix(BIB_SUFFIX)

  if str(path).count(sep) > 0:
    result = _search_file_by_path(path)
    if result:
      return result.absolute()
  else:
    search_list = [
      lambda: _search_file_in_current_directory(path, False),
      lambda: _search_file_in_bibinputs(path, False),
      lambda: _search_file_in_current_directory(path, True),
      lambda: _search_file_in_bibinputs(path, True),
    ]
    for search in search_list:
      result = search()
      if result:
        return result.absolute()

  error_msg = f'ファイルが見つかりません ({query})'
  if str(path).count(sep) == 0:
    error_msg += ', 環境変数 "BIBINPUTS" の内容が正しいかあわせて確認してください'
  raise FileNotFoundError(error_msg)

# pybtexのentriesディレクトリからkeyが一致するエントリを探して返す
# 完全一致するものがない場合は部分一致で探して返す
def search_entry(entries, key) -> Entry:
  entry = entries.get(key)

  if entry is None:
    suggestions = list(filter(lambda k: key.lower() in k.lower(), entries.keys()))
    if len(suggestions) == 1:
      entry = entries.get(suggestions[0])
    elif len(suggestions) > 1:
      raise KeyError(f'エントリが一意に定まりません ({key}) (候補: {", ".join(suggestions)})')
    else:
      raise KeyError(f'エントリが見つかりません ({key})')

  return entry
