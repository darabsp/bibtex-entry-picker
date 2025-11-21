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
  # TODO: オプション単体の場合は4人以上, 数値が指定されていれば指定された人数以上でet al.を出力する
  parser.add_argument(
    '-e', '--et-al',
    action='store_const',
    const=2,
    default=None,
    help='著者が複数人いる場合に第一著者のみを出力する',
  )

  return parser.parse_args()
