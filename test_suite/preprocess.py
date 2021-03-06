"""

A class for reading the contents of a file, modifying it in
memory, and writing it back.

A Filist is a list of strings that contains the contents of
a file.  All the usual list operations can be applied to a Filist.

Because this class loads the entire file into memory, it uses
more space than it might need to, and it is limited to working with
files that fit into memory.  The advantage is that it is easy to
implement algorithms that need random access to the contents of the
file, and it is convenient to debug because all the data is
available all the time.

Some of the methods I included are here because of specific
operations I was interested in.

Copyright 2012 Allen B. Downey
MIT License: http://opensource.org/licenses/mit-license.php
"""

import sys
import re

class Filist(list):
    def __init__(self, filename=None, t=None):
        """ if a filename is provided, read the contents """
        if filename:
            self.filename = filename
            lines = open(filename).readlines()
            self.extend(lines)
        # add any lines that are provided
        if t:
            self.extend(t)

    def __str__(self):
        return ''.join(self)

    def join(self):
        """collapse the list of strings into a single long string"""
        self[:] = [str(self)]

    def search_lines(self, pattern):
        """Traverse lines in order until one of them matches,
        return the index and the match object
        """
        pat = re.compile(pattern)
        for i in range(0, len(self)):
            match = pat.search(self[i])
            if match:
                return i, match

    def sub_lines(self, pattern, replace):
        """Traverse the lines and replace pattern with replace.

        pattern: regexp
        replace: replacement string
        """
        pat = re.compile(pattern)
        for i, line in enumerate(self):
            line, n = pat.subn(replace, self[i])
            if n:
                self[i] = line

    def clean_lines(self, func):
        """Traverse the lines and replace pattern with replace.

        func: function applied to each line
        """
        for i, line in enumerate(self):
            self[i] = func(line)

    def prefile(self, filename):
        """prepend the contents of the given file"""
        ft = Filist(filename)
        self.insert(0, ft)

    def suffile(self, filename):
        """append the contents of the given file"""
        ft = Filist(filename)
        self.extend(ft)

    def writeto(self, filename):
        """write the contents of the Filist to a file"""
        fp = open(filename, 'w')
        for line in self:
            fp.write(line)

    def writeback(self):
        """write the contents of the Filist back to the file it came from"""
        self.writeto(self.filename)


def change_suffix(filename, suffix):
    """return a new filename that is the same as the given name
    with the file extension replaced with the given suffix
    """
    filename.split('.')
    t[-1] = suffix
    return '.'.join(t)


def cp(source, dest):
    """copy a file from source to destination, returning a Filist"""
    ft = Filist(source)
    ft.writeto(dest)
    return ft


def encode_utf8_to_iso88591(utf8_text):
    '''
    This is a modified version of code from
    http://www.jamesmurty.com/2011/12/30/python-code-utf8-to-latin1/

    Encode and return the given UTF-8 text as LaTeX commands.

    If the given value is not a string it is returned unchanged.

    References:
    en.wikipedia.org/wiki/Quotation_mark_glyphs#Quotation_marks_in_Unicode
    en.wikipedia.org/wiki/Copyright_symbol
    en.wikipedia.org/wiki/Registered_trademark_symbol
    en.wikipedia.org/wiki/Sound_recording_copyright_symbol
    en.wikipedia.org/wiki/Service_mark_symbol
    en.wikipedia.org/wiki/Trademark_symbol
    '''
    if not isinstance(utf8_text, basestring):
        return utf8_text

    # Replace "smart" and other single-quote like things
    utf8_text = re.sub(
        u'[\u2018]',
        "`", utf8_text)

    utf8_text = re.sub(
        u'[\u2019]',
        "'", utf8_text)

    # Replace "smart" and other double-quote like things
    utf8_text = re.sub(
        u'[\u201c]',
        "``", utf8_text)

    utf8_text = re.sub(
        u'[\u201d]',
        "''", utf8_text)

    # Replace copyright symbol
    utf8_text = re.sub(u'[\u00a9\u24b8\u24d2]', r'\copyright', utf8_text)

    # Replace registered trademark symbol
    utf8_text = re.sub(u'[\u00ae\u24c7]', 
                       r'\textsuperscript{\textregistered}',
                       utf8_text)

    # Replace sound recording copyright symbol
    utf8_text = re.sub(u'[\u2117\u24c5\u24df]', r'\textcircledP', utf8_text)

    # Replace trademark symbol
    utf8_text = re.sub(u'[\u2122]', r'\texttrademark', utf8_text)

    return utf8_text


def main(name, filename, *argv):
    # print the contents of the given file
    ft = Filist(filename)

    # TODO: this is not working.  I need to investigate what the
    # special chars are that are in the Data Analysis files
    # ft.clean_lines(encode_utf8_to_iso88591)

    # TODO: if this pattern is split across lines, it will not get caught.
    ft.sub_lines(r'Chapter.\\ref', r'\\ref')
    ft.sub_lines(r'Section.\\ref', r'\\ref')
    ft.sub_lines(r'Figure.\\ref', r'\\ref')
    ft.sub_lines(r'Exercise.\\ref', r'\\ref')
    print ft


if __name__ == '__main__':
    main(*sys.argv)
