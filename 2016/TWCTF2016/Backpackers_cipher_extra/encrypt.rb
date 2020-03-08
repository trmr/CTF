require 'openssl'
require 'securerandom'

def random_bits(bits)
  loop do
    ret = SecureRandom.random_number(1 << bits)
    return ret if ret.to_s(2).size == bits
  end
end

def aes_encrypt(key, iv, message)
  enc = OpenSSL::Cipher.new('AES-128-CBC')
  enc.encrypt
  enc.key = key
  enc.iv = iv
  enc.update(message) + enc.final
end

def aes_decrypt(key, iv, message)
  enc = OpenSSL::Cipher.new('AES-128-CBC')
  enc.decrypt
  enc.key = key
  enc.iv = iv
  enc.update(message) + enc.final
end


def create_key(t = 128, nn_bits = 240, n = 300)
  nn = random_bits(nn_bits)
  s = Array.new(n) { SecureRandom.random_number(nn + 1) }
  sigma = s.inject(:+)
  z = 2 ** t
  p = nil
  while true
    p = SecureRandom.random_number(sigma - 1) + sigma + 1
    break if OpenSSL::BN.new(p.to_s(16), 16).prime?
  end
  e = SecureRandom.random_number(p / 2) + p / 2 + 1
  a = s.map{|s| e * s % p }
  b = s.map{|s| s % z}
  [[s, p, e], [a, b, z, n]]
end

def encrypt(pubkey, message)
  a, b, z, n = pubkey
  x = Array.new(n){SecureRandom.random_number(2)}
  key = (x.zip(b).map{|x,b|x*b}.inject(:+) % z) # This is secret
  encrypted_key = x.zip(a).map{|x,a|x*a}.inject(:+)
  encrypted_message = aes_encrypt(['%032x' % key].pack("H*"), [encrypted_key.to_s(16)].pack("H*"), message)
  [encrypted_key, encrypted_message]
end

def decrypt(privkey, pubkey, encrypted_key, encrypted_message)
  s, p, e = privkey
  a, b, z, n = pubkey
  einv = OpenSSL::BN.new(e.to_s(16), 16).mod_inverse(OpenSSL::BN.new(p.to_s(16), 16)).to_i
  key = (einv * encrypted_key % p) % z
  aes_decrypt(['%032x' % key].pack("H*"), [encrypted_key.to_s(16)].pack("H*"), encrypted_message)
end

message = File.read('flag')

privkey, pubkey = create_key

File.write('privkey', privkey.inspect)
File.write('pubkey', pubkey.inspect)

enc_key, encrypted = encrypt(pubkey, message)

File.write('encrypted_flag', [enc_key, encrypted].inspect)

fail if decrypt(privkey, pubkey, enc_key, encrypted) != message
