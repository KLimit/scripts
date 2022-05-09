#!/usr/bin/python3
"""Regex search through all excel files in a directory, recursive."""

import argparse
import pathlib
import re
import sys

import openpyxl
import zipfile


def excelgrep(filename, pattern, onlymatching, delimiter):
    """Search through each row of the given Excel file (first workbook)."""
    book = openpyxl.load_workbook(filename)
    sheet = book.active
    matches = 0
    print(str(filename) + delimiter*(sheet.max_column-1))
    for row in sheet.rows:
        for cell in row:
            search = re.search(pattern, str(cell.value), re.I)
            if search:
                line = cell.value if onlymatching else stringrow(row, delimiter)
                print(line)
                matches += 1
    return matches


def stringrow(row, delimiter=','):
    """Convert a whole row to a string with delimiter."""
    return delimiter.join(fmtcell(cell, delimiter) for cell in row)


def fmtcell(cell, delimiter):
    """Format a cell into printable format, respecting the delimiter."""
    cell = str(cell.value)
    if delimiter in cell:
        cell = '"' + cell + '"'
    return cell


def main():
    """Grep through each given workbook for given pattern."""
    pser = argparse.ArgumentParser()
    pser.add_argument('filepattern')
    pser.add_argument('greppattern')
    pser.add_argument('-o', '--only-matching', action='store_true')
    pser.add_argument('-d', '--delimiter', default=',')
    args = pser.parse_args()
    for path in sorted(pathlib.Path('.').rglob(args.filepattern)):
        try:
            matches = excelgrep(
                path,
                args.greppattern,
                args.only_matching,
                args.delimiter,
            )
        except zipfile.BadZipFile:
            sys.stderr.write('Cannot read zip file.\n')
            matches = 0
        if not matches:
            sys.stderr.write('No matches\n')
    return 0 if matches else 1


if __name__ == '__main__':
    main()
