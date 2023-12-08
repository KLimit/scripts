use strict;
use warnings;

print "[\r\n";
while(<>) {
	chomp;
	s/'/"/g;
	s/True/true/g;
	s/False/false/g;
	s/None/null/g;
	print;
	print "," if not eof;
	print "\r\n";
}
print "]\r\n";
