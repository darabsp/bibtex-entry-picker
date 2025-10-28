from pybtex.database import parse_file
from pybtex.style.formatting.plain import Style as PlainStyle
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
    raise KeyError(f'キーが一致するエントリが見つかりません ({entry_key})')

  formatted = PlainStyle().format_entry(None, entry).text.render_as('text')

  pyperclip.copy(formatted)
  print(f'コピーしました: {formatted}')

if __name__ == '__main__':
  try:
    main(args=sys.argv)
  except BaseException as e:
    sys.exit(f'エラーが発生しました ({e.__class__.__name__}): {" ".join(e.args)}')
