# Acknowledgement:
#
# The output of this formatting style is inspired by junsrt style from pbibtex.
# And the implementation of this formatting style is based on unsrt.py from Pybtex package.
# Pybtex package is published under the following, MIT License:
#
#   Copyright (c) 2006-2021  Andrey Golovizin
#
#   Permission is hereby granted, free of charge, to any person obtaining
#   a copy of this software and associated documentation files (the
#   "Software"), to deal in the Software without restriction, including
#   without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to
#   permit persons to whom the Software is furnished to do so, subject to
#   the following conditions:
#
#   The above copyright notice and this permission notice shall be
#   included in all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from pybtex.style.formatting import BaseStyle, toplevel
from pybtex.style.names import BaseNameStyle, name_part
from pybtex.style.template import optional_field, field, join, names, optional, sentence, words
from regex import search

class CJKUtils():
  # upBibTeXのis.kanji.strを参考にひらがな/カタカナ/漢字/ハングルを含む文字列/エントリを判定
  def is_cjk_string(self, string):
    return search(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}\p{Script=Hangul}]+', string) is not None

  def is_cjk_entry(self, entry):
    about_persons = [self.is_cjk_string(str(person)) for person in entry.persons.values()]
    about_fields = [self.is_cjk_string(field) for field in entry.fields.values()]
    return any(about_persons) or any(about_fields)

class NameStyle(BaseNameStyle, CJKUtils):
  def format(self, person, abbr=False):
    tie = not self.is_cjk_string(str(person))
    abbr = abbr and not self.is_cjk_string(str(person))
    return join [
      name_part(tie=tie, abbr=abbr) [person.rich_first_names + person.rich_middle_names],
      name_part(tie=tie) [person.rich_prelast_names],
      name_part [person.rich_last_names],
      name_part(before=', ') [person.rich_lineage_names],
    ]

class Style(BaseStyle, CJKUtils):
  def __init__(self, label_style=None, name_style=None, sorting_style=None, abbreviate_names=False, min_crossrefs=2, et_al=None, **kwargs):
    self.default_name_style = NameStyle
    self.et_al = et_al
    super().__init__(label_style, name_style, sorting_style, abbreviate_names, min_crossrefs, **kwargs)

  # 各項目の整形

  def format_date(self, _):
    return words [optional_field('month'), field('year')]

  def format_first_person(self, entry, field_type):
    return self.format_name(entry.persons[field_type][0], self.abbreviate_names)

  def format_persons(self, entry, field_type):
    if self.is_cjk_entry(entry):
      return names(field_type, sep=', ', sep2=', ', last_sep=', ')
    else:
      return names(field_type, sep=', ', sep2=' and ', last_sep=', and ')

  def format_author(self, entry, field_type='author'):
    if self.et_al is not None and len(entry.persons[field_type]) >= self.et_al:
      if self.is_cjk_entry(entry):
        return words('') [self.format_first_person(entry, field_type), 'ら']
      else:
        return words [self.format_first_person(entry, field_type), 'et al.']
    else:
      return self.format_persons(entry, field_type)

  def format_booktitle(self, entry, field_type='booktitle'):
    if self.is_cjk_entry(entry):
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
    if self.is_cjk_entry(entry):
      return words(' ') [
        self.format_persons(entry, field_type),
        '編,',
      ]
    else:
      return words(', ') [
        self.format_persons(entry, field_type),
        'editor,' if field_count == 1 else 'editors,',
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
      sentence [optional_field('note')],
    ]

  def get_inproceedings_template(self, entry):
    return toplevel [
      sentence [self.format_author(entry)],
      sentence [field('title')],
      sentence [
        self.format_booktitle(entry),
        optional [self.format_volume(entry)],
        optional [self.format_number(entry)],
        optional [self.format_pages(entry)],
        optional [self.format_date(entry)],
      ],
      sentence [optional_field('note')],
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
      sentence [optional_field('note')],
    ]

  def get_misc_template(self, entry):
    return toplevel [
      sentence [self.format_author(entry)],
      sentence [field('title')],
      sentence [optional_field('howpublished')],
      sentence [optional_field('note')],
    ]
