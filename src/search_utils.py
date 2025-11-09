import os
from pybtex.database import Entry

def _search_file_by_path(path: str) -> str | None:
  if os.path.isfile(path):
    return path
  else:
    return None

def _search_file_in_bibinputs(filename: str) -> str | None:
  bibinputs = os.environ.get('BIBINPUTS')
  if bibinputs is None:
    return None

  directories = [directory for directory in bibinputs.split(os.pathsep) if os.path.isdir(directory)]
  if directories == []:
    return None

  for directory in directories:
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
      return path

  return None

# .bibファイルを探してそのpathを返す
# パスが入力された場合 (e.g. ../bibtex/biblio.bib): 指定されたパスのみ検索, 環境変数の検索は行わない
# ファイル名のみが入力された場合 (e.g. biblio.bib, biblio): カレントディレクトリと環境変数を検索
def search_bib_file(input_path: str) -> str:
  query = input_path if input_path.endswith('.bib') else input_path + '.bib'

  result = _search_file_by_path(query)
  if result is not None:
    return result

  if os.path.dirname(query) == '':
    result = _search_file_in_bibinputs(query)
    if result is not None:
      return result

  error_msg = f'ファイルが見つかりません ({input_path})'
  if os.path.dirname(query) == '':
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
