#! /usr/bin/perl
use strict;
use warnings;

# keep saving the latest name. If the next item is just a number, prepend the
# current name

my $currentname = '';
my $numpttn = /_?\d*/;

while(<>) {
	$currentname = s/$numpttn//;
}
