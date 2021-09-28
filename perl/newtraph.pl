#! /opt/local/bin/perl

# Simple (misnamned) script to extract the positive square root of a 
# number (the "radicand").

print "Enter radicand:\n";
chomp($x = <STDIN>);
print "radicand = $x\n";
print "Enter first approximation:\n";
chomp($xi = <STDIN>);
print "first approximation = $xi\n\n";
if (($x <= 0.0) or ($xi <= 0.0)) {die "Both params must be positive.\n"}
for ($i = 0; $i < 10; $i++) {
	print "x[", $i, "] = ", $xi, "\n";
	$xi = ($xi + ($x/$xi))/2;
}
exit 0;
