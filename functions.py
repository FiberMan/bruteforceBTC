import binascii, hashlib, base58, ecdsa

# Creates a bitcoin address from hashed public key
def getAddress(pub_key_hashed_bytes):
    # Prefix 0x00 - indicates main network address
    # Prefix 0x6F - indicates test network address
    fullkey = b"\x00" + pub_key_hashed_bytes
    sha256a = hashlib.sha256(fullkey).digest()
    sha256b = hashlib.sha256(sha256a).digest()
    checksum = sha256b[:4]
    return base58.b58encode(fullkey+checksum).decode()

# The WIF is used for import/export of keys between wallets and often used in QR code (barcode) representations of private keys.
def getWIF(priv_key_bytes, compressed=False):
    # Prefix 0x80 - indicates WIF address
    # Suffix 0x01 - denotes that the private key within will be used to produce compressed public keys only
    fullkey = b"\x80" + priv_key_bytes + (b"\x01" if compressed else b"")
    sha256a = hashlib.sha256(fullkey).digest()
    sha256b = hashlib.sha256(sha256a).digest()
    checksum = sha256b[:4]
    return base58.b58encode(fullkey+checksum).decode()

# Applies Elliptic Curve Digital Signature Algorithm to get a public key from private key
def getPubKey(priv_key_bytes):
    sk = ecdsa.SigningKey.from_string(priv_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return vk.to_string()

# Creates full uncompressed public key
def getPubKeyFullUncompressed(pub_key_bytes):
    # Prefix 0x04 indicates that public key is uncompressed
    return b"\x04" + pub_key_bytes

# Creates full compressed public key
def getPubKeyFullCompressed(pub_key_bytes):
    half_len = len(pub_key_bytes) // 2
    key_half = pub_key_bytes[:half_len]
    # Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
    last_byte = pub_key_bytes[-1]
    bitcoin_byte = b"\x02" if last_byte % 2 == 0 else b"\x03"
    return bitcoin_byte + key_half

# Perform SHA-256 and RipeMD160 hash functions
def getPubKeyHashed(pub_key_full_bytes):
    sha256 = hashlib.sha256(pub_key_full_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256)
    return ripemd160.digest()

# Validate Bitcoin address
def validateAddress(bitcoinAddress):
    print("--------------------------------------")
    print("Bitcoin Address: ", bitcoinAddress)
    # base58.b58decode method generate Byte and we should convert it to Hex with hex() method
    base58Decoder = base58.b58decode(bitcoinAddress).hex()
    print("Base58 decoded:  ", base58Decoder)
    prefix = base58Decoder[:2]
    hash = base58Decoder[2:len(base58Decoder)-8]
    checksum = base58Decoder[len(base58Decoder)-8:]
    print("\tPrefix:   ", prefix)
    print("\tHash:     ", hash)
    print("\tChecksum: ", checksum)
    print("--------------------------------------")
    # to handle true result, we should pass our input to hashlib.sha256() method() as Byte format
    # so we use binascii.unhexlify() method to convert our input from Hex to Byte
    # finally, hexdigest() method convert value to human-readable
    hash = prefix + hash
    for x in range(1,3):
        hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
        print("Hash#", x, " : ", hash)
    print("--------------------------------------")
    if(checksum == hash[:8]):
        print("[TRUE]  checksum is valid!")
    else:
        print("[FALSE] checksum is not valid!")