#!/usr/bin/env bash
# Remove the first line of a file if there is only one comma in it.
# this is used for poorly-formed CSVs that have an extra date entry at the
# start of the file. Note that empty lines at the start of the file must
# first be removed in order for this to work.

read filename
if [[ $(head -n 1 "$filename" | tr -d -c ',' | wc -m) = 1 ]]; then
	tail -n +2 "$filename" > tmp && mv tmp "$filename"
	echo "Deleted first line of $filename"
fi
