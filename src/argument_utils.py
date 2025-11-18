from argparse import ArgumentParser

def parse_args():
  parser = ArgumentParser()
  parser.add_argument(
    'bib',
    help='エントリが含まれるbibファイルのパス, またはファイル名',
  )
  parser.add_argument(
    'key',
    help='コピーするエントリのキー',
  )
  parser.add_argument(
    '-e', '--et-al',
    action='store_const',
    const=4,
    default=None,
    help='著者が4人以上いる場合に第一著者のみを出力する',
  )

  return parser.parse_args()
