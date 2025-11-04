# pybtexのunsrtフォーマットスタイルのソースコードを参考に作成

from pybtex.style.formatting import *
from pybtex.style.template import *
import regex

class Style(BaseStyle):
  # upBibTeXのis.kanji.strを参考にひらがな/カタカナ/漢字を含むエントリを日本語によるエントリとする
  def is_japanese_string(self, string):
    return regex.search(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]+', string) is not None

  def is_japanese_entry(self, entry):
    about_persons = [self.is_japanese_string(str(person)) for person in entry.persons.values()]
    about_fields = [self.is_japanese_string(field) for field in entry.fields.values()]
    return any(about_persons) or any(about_fields)

  # 各項目の整形

  def format_date(self, _):
    return words [optional_field('month'), field('year')]

  def format_persons(self, entry, field_type):
    if self.is_japanese_entry(entry):
      return names(field_type, sep=', ', sep2=', ', last_sep=', ')
    else:
      return names(field_type, sep=', ', sep2=' and ', last_sep=', and ')

  def format_author(self, entry, field_type='author'):
    return self.format_persons(entry, field_type)

  def format_booktitle(self, entry, field_type='booktitle'):
    if self.is_japanese_entry(entry):
      return words [
        optional [self.format_editor(entry)],
        field(field_type),
      ]
    else:
      return words [
        'In',
        optional [self.format_editor(entry)],
        field(field_type),
      ]

  def format_editor(self, entry, field_type='editor'):
    raw_field = entry.persons.get(field_type)
    field_count = len(raw_field) if raw_field is not None else 0
    if self.is_japanese_entry(entry):
      return words(' ') [
        self.format_persons(entry, field_type),
        '編',
      ]
    else:
      return words(', ') [
        self.format_persons(entry, field_type),
        'editor' if field_count == 1 else 'editors',
      ]

  def format_number(self, _, field_type='number'):
    return words ['No.', field(field_type)]

  def format_pages(self, entry, field_type='pages'):
    raw_field = entry.fields.get(field_type)
    index = raw_field.find('--') if raw_field is not None else -1
    if index == -1:
      return words ['p.', raw_field]
    else:
      return words ['pp.', raw_field.replace('--', '–')]

  def format_volume(self, _, field_type='volume'):
    return words ['Vol.', field(field_type)]

  # エントリの整形

  def get_article_template(self, entry):
    return toplevel [
      sentence [self.format_author(entry)],
      sentence [field('title')],
      sentence [
        field('journal'),
        optional [self.format_volume(entry)],
        optional [self.format_number(entry)],
        self.format_pages(entry),
        optional [self.format_date(entry)],
      ],
    ]

  def get_inproceedings_template(self, entry):
    return toplevel [
      sentence [self.format_author(entry)],
      sentence [field('title')],
      sentence [
        self.format_booktitle(entry),
        optional [self.format_volume(entry)],
        optional [self.format_number(entry)],
        optional [self.format_date(entry)],
      ],
    ]

  def get_mastersthesis_template(self, entry):
    return toplevel [
      sentence [self.format_author(entry)],
      sentence [field('title')],
      sentence [
        optional_field('type'),
        field('school'),
        optional [self.format_date(entry)],
      ],
    ]
