from formatting_style import Style
from pybtex.database import parse_file
import os
import pyperclip
import sys

def main(args) -> None:
  if len(args) < 3:
    raise ValueError(f'引数が不足しています ({len(args)})')
  if len(args) > 3:
    raise ValueError(f'引数が多すぎます ({len(args)})')

  bibfile_path = args[1]
  entry_key = args[2]

  if not os.path.isfile(bibfile_path):
    raise FileNotFoundError(f'ファイルが見つかりません ({bibfile_path})')

  bibfile = open(bibfile_path)
  bib = parse_file(bibfile)
  entry = bib.entries.get(entry_key)

  if entry is None:
    autocomplete = list(filter(lambda key: entry_key.lower() in key.lower(), bib.entries.keys()))
    if len(autocomplete) == 1:
      entry = bib.entries.get(autocomplete[0])
    elif len(autocomplete) > 1:
      raise KeyError(f'エントリが一意に定まりません ({entry_key}) (候補: {", ".join(autocomplete)})')
    else:
      raise KeyError(f'エントリが見つかりません ({entry_key})')

  formatted = Style().format_entry(None, entry).text.render_as('text')

  pyperclip.copy(formatted)
  print(f'コピーしました: {formatted}')

if __name__ == '__main__':
  try:
    main(args=sys.argv)
  except BaseException as e:
    sys.exit(f'エラーが発生しました ({e.__class__.__name__}): {" ".join(e.args)}')
