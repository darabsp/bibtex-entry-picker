from formatting_style import Style
from search_utils import search_bib_file, search_entry
from pybtex.database import parse_file
import pyperclip
import sys

def main(args) -> None:
  if len(args) < 3:
    raise ValueError(f'引数が不足しています ({len(args)})')
  if len(args) > 3:
    raise ValueError(f'引数が多すぎます ({len(args)})')

  path = search_bib_file(args[1])
  key = args[2]

  bib = parse_file(path)
  entry = search_entry(bib.entries, key)
  formatted = Style().format_entry(None, entry).text.render_as('text')

  pyperclip.copy(formatted)
  print(f'コピーしました: {formatted}')

if __name__ == '__main__':
  try:
    main(args=sys.argv)
  except BaseException as e:
    sys.exit(f'エラーが発生しました ({e.__class__.__name__}): {" ".join(e.args)}')
