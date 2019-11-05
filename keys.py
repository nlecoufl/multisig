import os, binascii, hashlib, base58, ecdsa
import random
import qrcode
import struct
from hexdump import hexdump

# Generating Private key, Public keys, WIF and Public address

# hexlify
# -> return hexadecimal representation of binary data
def shex(x):
  return binascii.hexlify(x).decode()

def sha256(x):
  return hashlib.sha256(x).digest()

def checksum(x):
  return sha256(sha256(x))[:4]

def ripemd160(x):
  d = hashlib.new('ripemd160')
  d.update(x)
  return d

def base58_w_checksum(x):
  return base58.b58encode(x+checksum(x))

def make_private_key(seed):
  # use seed for debugging
  random.seed(seed)
  # generate entropy
  return bytes([random.randint(0, 256) for x in range(32)])

# use full key to generate WIF
def get_full_key(priv_key):
  # prefix -> mainnet: 0x80 - testnet: 0xef
  prefix = b'\xef'
  return prefix + priv_key

def priv_to_publ_key(priv_key):
  sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
  vk = sk.get_verifying_key()
  return b'\x04' + vk.to_string()

def get_publ_address(publ_key):
  # prefix -> mainnet: 0x00 - testnet: 0x6f
  prefix = b'\x6f'
  hash160 = ripemd160(sha256(publ_key)).digest()
  full_hash = prefix + hash160
  publ_addr = base58_w_checksum(full_hash)
  return publ_addr

# Here is the doc to generate WIF
# https://en.bitcoin.it/wiki/Wallet_import_format
def get_keys_w_seed(seed):
  priv_key = make_private_key(seed)
  full_key = get_full_key(priv_key)
  WIF = base58_w_checksum(full_key).decode()
  publ_key = priv_to_publ_key(priv_key)
  publ_addr = get_publ_address(publ_key)
  return priv_key, publ_key, WIF, publ_addr

print(get_keys_w_seed(0))
# You can verify here by pasting WIF: https://coinb.in/#verify

