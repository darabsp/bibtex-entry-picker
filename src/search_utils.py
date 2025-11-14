import os
from pybtex.database import Entry

def _search_file_by_path(path: str) -> str | None:
  if os.path.isfile(path):
    return path

  return None

def _search_file_in_current_directory(filename: str, partial_search: bool) -> str | None:
  if os.path.isfile(filename):
    return os.path.abspath(filename)

  if partial_search:
    all_bib_files = [fn for fn in os.listdir() if os.path.isfile(fn)]
    suggestions = [fn for fn in all_bib_files if filename.removesuffix('.bib').lower() in fn.lower()]
    if len(suggestions) == 1:
      return os.path.abspath(suggestions[0])

  return None

def _search_file_in_bibinputs(filename: str, partial_search: bool) -> str | None:
  bibinputs = os.environ.get('BIBINPUTS')
  if bibinputs is None:
    return None

  directories = [directory for directory in bibinputs.split(os.pathsep) if os.path.isdir(directory)]
  if directories == []:
    return None

  all_bib_files = []
  for directory in directories:
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
      return os.path.abspath(path)

    all_bib_files.extend([os.path.join(directory, fn) for fn in os.listdir(directory) if os.path.isfile(os.path.join(directory, fn)) and fn.endswith('.bib')])

  if partial_search:
    suggestions = [fn for fn in all_bib_files if filename.removesuffix('.bib').lower() in fn.lower()]
    if len(suggestions) == 1:
      return os.path.abspath(suggestions[0])

  return None

# .bibファイルを探してそのpathを返す
# パスが入力された場合 (e.g. ../bibtex/biblio.bib): 指定されたパスのみ検索, 環境変数の検索は行わない
# ファイル名のみが入力された場合 (e.g. biblio.bib, biblio): カレントディレクトリと環境変数を検索
def search_bib_file(query: str) -> str:
  corrected_query = query if query.endswith('.bib') else query + '.bib'
  dirname = os.path.dirname(corrected_query)
  filename = os.path.basename(corrected_query)
  fullpath = os.path.join(dirname, filename)

  if dirname != '':
    result = _search_file_by_path(fullpath)
    if result is not None:
      return result
  else:
    result = _search_file_in_current_directory(filename, False)
    if result is not None:
      return result
    result = _search_file_in_bibinputs(filename, False)
    if result is not None:
      return result
    result = _search_file_in_current_directory(filename, True)
    if result is not None:
      return result
    result = _search_file_in_bibinputs(filename, True)
    if result is not None:
      return result

  error_msg = f'ファイルが見つかりません ({query})'
  if dirname == '':
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
