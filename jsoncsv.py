#!/usr/bin/env python3
import csv
import json
import sys


def main():
    dl = json.load(sys.stdin)
    writer = csv.DictWriter(sys.stdout, dl[0].keys())
    writer.writeheader()
    writer.writerows(dl)


if __name__ == "__main__":
    sys.exit(main())

