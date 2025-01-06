"""
This module allows for the renumbering of the headers in a markdown file.
 when the headers of a markdown file have been manually added,
 and some of those headers are deleted,
 it can cause gaps in the numbering.

Headers have to follow the format "LetterNumber. Title".

Limitations:
 + This module doesn't support hierarchical outlines/numbering.
 + This module doesn't support advanced numbering scheme.
"""

from re import Match, compile
import sys
from fileinput import input as finput  # Warning: print() will write to file!


header_num = 0
HEADER_RE = compile(r"(#{1,6}) ([A-Za-z])(\d+)\. (.*)")

def process_md_line(md_line: str) -> str:

    global header_num
    md_line_processed = ""

    def renumber_header(h_mo: Match) -> str:
        return f"{h_mo.group(1)} {h_mo.group(2)}{header_num}. {h_mo.group(4)}\n"

    if header_mo := HEADER_RE.match(md_line):
        header_num += 1
        md_line_processed = renumber_header(header_mo)
    else:
        md_line_processed = md_line

    return md_line_processed


def main():

    argn_cmd = len(sys.argv)-1
    argv_cmd = sys.argv[1:]

    if argn_cmd == 1:
        file_path = argv_cmd[0]
        for md_line in finput(file_path, inplace=1, encoding='utf-8'):
            sys.stdout.write(process_md_line(md_line))
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} file")

if __name__ == '__main__':
    main()