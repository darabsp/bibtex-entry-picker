from argument_utils import parse_args
from formatting_style import Style
from search_utils import search_bib_file, search_entry
from pybtex.database import parse_file
import pyperclip
import sys

def main() -> None:
  try:
    args = parse_args()
    path = search_bib_file(args.bib)
    key = args.key

    bib = parse_file(path)
    entry = search_entry(bib.entries, key)
    formatted = Style().format_entry(None, entry).text.render_as('text')

    pyperclip.copy(formatted)
    print(f'コピーしました: {formatted}')
  except SystemExit as e:
    sys.exit(e.code)
  except BaseException as e:
    sys.exit(f'エラーが発生しました ({e.__class__.__name__}): {" ".join(map(str, e.args))}')

if __name__ == '__main__':
  main()
