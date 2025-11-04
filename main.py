from formatting_style import Style
from pybtex.database import parse_file, Entry
import os
import pyperclip
import sys

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

def main(args) -> None:
  if len(args) < 3:
    raise ValueError(f'引数が不足しています ({len(args)})')
  if len(args) > 3:
    raise ValueError(f'引数が多すぎます ({len(args)})')

  bibfile_path = args[1]
  key = args[2]

  if not os.path.isfile(bibfile_path):
    raise FileNotFoundError(f'ファイルが見つかりません ({bibfile_path})')

  bibfile = open(bibfile_path)
  bib = parse_file(bibfile)
  entry = search_entry(bib.entries, key)
  formatted = Style().format_entry(None, entry).text.render_as('text')

  pyperclip.copy(formatted)
  print(f'コピーしました: {formatted}')

if __name__ == '__main__':
  try:
    main(args=sys.argv)
  except BaseException as e:
    sys.exit(f'エラーが発生しました ({e.__class__.__name__}): {" ".join(e.args)}')
