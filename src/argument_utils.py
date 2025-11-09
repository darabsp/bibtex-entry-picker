import argparse

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'bib',
    help='エントリが含まれるbibファイルのパス, またはファイル名',
  )
  parser.add_argument(
    'key',
    help='コピーするエントリのキー',
  )
  return parser.parse_args()
