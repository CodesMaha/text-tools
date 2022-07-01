"""
This module allows to renumber the headers of a Markdown file
 when these headers have been manually numbered
 and some headers have been deleted,
 causing gaps in the numbering.
These headers have to follow the format "LetterNumber. Title".
Limitations:
 + This module doesn't support hierarchical outlines/numbering.
 + This module doesn't support advanced numbering scheme.
"""

import re
import sys
import fileinput  # Warning: print() will write to file!


header_num = 0
HEADER_RE = re.compile(r"(#{1,6}) ([A-Za-z])(\d+)\. (.*)")

def process_md_line(md_line:str) -> str:

    global header_num
    md_line_processed = ""

    def renumber_header(h_mo:re.Match) -> str:
        return f"{h_mo.group(1)} {h_mo.group(2)}{header_num}. {h_mo.group(4)}\n"

    if header_mo := HEADER_RE.match(md_line):
        header_num = header_num + 1
        md_line_processed = renumber_header(header_mo)
    else:
        md_line_processed = md_line

    return md_line_processed


def main():
    argn_cmd = len(sys.argv)-1
    argv_cmd = sys.argv[1:]
    if argn_cmd == 1:
        file_path = argv_cmd[0]
        for md_line in fileinput.input(file_path, inplace=1, encoding='utf-8'):
            sys.stdout.write(process_md_line(md_line))
    else:
        raise SystemExit(f"Usage: {sys.argv[0]} file")

if __name__ == '__main__':
    main()