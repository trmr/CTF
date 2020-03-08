require 'openssl'
require 'json'

module BackpackCipher
  def self.generate_key(n = 1024)
    fail if n % 64 != 0 # For DES
    m = 2 ** n
    a = Array.new(n) {|i| (rand(m/2**i)|1)*2**i}
    p = OpenSSL::BN.generate_prime(a.inject(:+).to_s(2).size + 1).to_i
    q = 0
    q = rand(p) while p.gcd(q) != 1 and q != 1
    return [a.map{|a|a*q%p}, [p,q]]
  end

  def self.encrypt(pubkey, message)
    raise StandardError.new("Too long message") if message.size >= pubkey.size / 8
    # randomize message
    pad = pubkey.size / 8 - message.size
    message += pad.chr * pad
    des = OpenSSL::Cipher.new('des-ecb')
    des.encrypt
    des.padding = 0
    des.key = 'testpass'
    message = format("%0#{pubkey.size}b", (des.update(message) + des.final).unpack("H*")[0].to_i(16))
    # encrypt
    pubkey.zip(message.chars).map{|a,b|a*b.to_i}.inject(:+)
  end

  def self.decrypt(privkey, pubkey, message)
    raise NotImplementedError.new("I'm tired")
  end
end

if ARGV[0] == 'genkey' && ARGV.size == 3
  pubkey, privkey = BackpackCipher.generate_key
  File.write(ARGV[1], pubkey.to_json)
  File.write(ARGV[2], privkey.to_json)
elsif ARGV[0] == 'encrypt' && ARGV.size == 4
  pubkey = JSON.parse(File.read(ARGV[1]))
  File.write(ARGV[3], BackpackCipher.encrypt(pubkey, File.binread(ARGV[2])))
elsif ARGV[0] == 'decrypt' && ARGV.size == 5
  pubkey = JSON.parse(File.read(ARGV[1]))
  privkey = JSON.parse(File.read(ARGV[2]))
  File.write(ARGV[4], BackpackCipher.decrypt(privkey, pubkey, File.binread(ARGV[3])))
else
  puts <<EOS
Usage:
ruby cipher.rb genkey <PUBKEY_FILE> <PRIVKEY_FILE>
ruby cipher.rb encrypt <PUBKEY_FILE> <MESSAGE_FILE> <DESTINATION_FILE>
ruby cipher.rb decrypt <PUBKEY_FILE> <PRIVKEY_FILE> <ENCRYPTED_FILE> <DESTINATION_FILE>
EOS
end
