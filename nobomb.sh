#!/usr/bin/sh
# Apply vim's set nobomb to all files in the current directory
vim -c ":bufdo set nobomb|update" -c "q" * 
