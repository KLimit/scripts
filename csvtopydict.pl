use strict;
use warnings;

print "NAME = {\r\n";
while(<>) {
	next if not /'/;
	my ($key, $value) = split('\t');
	print "    $key: $value,\r\n";
}
print "}\r\n";
