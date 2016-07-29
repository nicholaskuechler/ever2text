# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import str
import json
import os
import sys
from dateutil.parser import parse
from html2text import HTML2Text
from lxml import etree
from bs4 import BeautifulSoup


class EverConverter(object):
    """Evernote conversion runner
    """

    fieldnames = ['createdate', 'modifydate', 'content', 'tags']
    date_fmt = '%h %d %Y %H:%M:%S'

    def __init__(self, enex_filename, output_dir=None, fmt="text",
                 preserve_title=False, verbose=False):
        self.enex_filename = os.path.expanduser(enex_filename)
        self.stdout = False
        if output_dir is None:
            self.stdout = True
            self.output_dir = output_dir
        else:
            self.output_dir = os.path.expanduser(output_dir)
        self.fmt = fmt
        self.preserve_title = preserve_title
        self.verbose = verbose
        self.use_beautifulsoup = True

    def _load_xml(self, enex_file):
        try:
            parser = etree.XMLParser(huge_tree=True)
            xml_tree = etree.parse(enex_file, parser)
        except (etree.XMLSyntaxError, ) as e:
            print('Could not parse XML')
            print(e)
            sys.exit(1)
        return xml_tree

    def prepare_notes(self, xml_tree):
        notes = []
        raw_notes = xml_tree.xpath('//note')
        for note in raw_notes:
            note_dict = {}
            title = note.xpath('title')[0].text
            note_dict['title'] = title
            # Use dateutil to figure out these dates
            # 20110610T182917Z
            created_string = parse('19700101T000017Z')
            if note.xpath('created'):
                created_string = parse(note.xpath('created')[0].text)
            updated_string = created_string
            if note.xpath('updated'):
                updated_string = parse(note.xpath('updated')[0].text)
            note_dict['createdate'] = created_string.strftime(self.date_fmt)
            note_dict['modifydate'] = updated_string.strftime(self.date_fmt)
            tags = [tag.text for tag in note.xpath('tag')]
            note_dict['tags'] = tags
            note_dict['content'] = ''
            content = note.xpath('content')
            if content:
                raw_text = content[0].text
                # TODO: Option to go to just plain text, no markdown
                converted_text = self._convert_note_to_text(title, raw_text)
                note_dict['content'] = converted_text
                if self.verbose:
                    print("note_dict: {}".format(note_dict))
            notes.append(note_dict)
        return notes

    def convert(self):
        if not os.path.exists(self.enex_filename):
            print("File does not exist: {}".format(self.enex_filename))
            sys.exit(1)
        # TODO: use with here, but pyflakes barfs on it
        enex_file = open(self.enex_filename)
        xml_tree = self._load_xml(enex_file)
        enex_file.close()
        notes = self.prepare_notes(xml_tree)
        self._convert_dir(notes)

    def _convert_note_to_text(self, title, text):
        if self.fmt == "markdown":
            html2plain = HTML2Text(None, "")
            html2plain.feed("<h1>%s</h1>" % title)
            html2plain.feed(text)
            return html2plain.close()
        else:
            soup = BeautifulSoup(text, 'html.parser')
            output = soup.get_text()
            return output

    def sanitize_note_title(self, note_title):
        # replace spaces with underscores
        note_title = note_title.replace(' ', '_')
        # replace forward slaces with dashes
        note_title = note_title.replace('/', '-')
        note_title = note_title.replace('|', '-')
        note_title = note_title.replace('(', '')
        note_title = note_title.replace(')', '')
        note_title = note_title.replace('?', '')
        note_title = note_title.replace('*', '')
        note_title = note_title.replace('!', '')
        note_title = note_title.replace('$', '')
        note_title = note_title.replace('"', '')
        note_title = note_title.replace("'", '')
        note_title = note_title.replace(':', '-')
        note_title = note_title.replace('>', '-')
        note_title = note_title.replace('<', '-')
        note_title = note_title.replace('®', '')
        note_title = note_title.replace(u"\u2122", '')
        return note_title

    def _convert_dir(self, notes):
        if self.output_dir is None:
            sys.stdout.write(json.dumps(notes))
        else:
            if (os.path.exists(self.output_dir) and
                    not os.path.isdir(self.output_dir)):
                print('"{}" exists but is not a directory.'.format(
                  self.output_dir))
                sys.exit(1)
            elif not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            for i, note in enumerate(notes):
                if self.preserve_title:
                    # (nicholaskuechler) try to preserve the title, but replace
                    # spaces with underscores, replace forward slash with dash,
                    # and preserve the note number in case of duplicate titles.
                    note_title = note['title']
                    note_title = self.sanitize_note_title(note_title)
                    note_title = "%s-%s" % (note_title, i)
                else:
                    note_title = str(i)

                try:
                    output_file_path = \
                        os.path.join(self.output_dir, note_title + '.txt')
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(note['content'])
                except Exception as e:
                    output_file_path = os.path.join(
                        self.output_dir,
                        "title_fail" + '-' + str(i) + '.txt')
                    print("failed to use title for filename: {}".format(e))
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(note['content'])
