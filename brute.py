import datetime as dt
import os, multiprocessing
import base58
from functions import * 

threads=8
addressFile = 'addresses.txt'
foundFile = 'found.txt'

# Decode bitcoin address to get hashed public key without prefix (network byte) and checksum
def getRawAddress(bitcoinAddress):
    hex = base58.b58decode(bitcoinAddress)
    return hex[1:len(hex)-4]

# Create a set of hashed public keys decoded from provided list of bitcoin addresses
def createHashedPubKeySetFromAddressList(filename):
    addressList = []
    with open(filename) as f:
        for line in f:
            addressList.append(getRawAddress(line.strip('\n')))
    return set(addressList)

def searchInList(priv_key, hash160, rawAddressSet, compression, outputFile):
    if hash160 in rawAddressSet:
        address = getAddress(hash160)
        message = 'YEAH! Address %s is %s and has a private key: %s' % (address, compression, priv_key.hex())
        print(message)
        with open(outputFile,'a') as f:
            f.write(message + '\n')

def yearsToFindAkey(threadSpeed, threads, searchListSize):
    totalSpeed = threadSpeed * threads
    combinations = 2**160
    iterationsToSuccess = combinations / searchListSize
    return iterationsToSuccess / totalSpeed / 3600 / 24 / 365

def seek(thread, hash160Set):
    LOG_EVERY_N = 100000
    start_time = dt.datetime.today().timestamp()
    i = 0
    print("Thread %s:  Searching Private Key.." % thread)
    while True:
        i=i+1
        # generate private key
        priv_key = os.urandom(32)

        # To test if the script really works and not just heating your room
        # add some address with known private key to addresses.txt, i.e.:
        # Address uncompressed:  18CJdksq7eVGnENaackZDpMb4rgbc9YR7y
        # Address compressed:    17JsmEygbbEUEpvt4PFtYaTeSqfb9ki1F1
        # and uncomment following lines specifying appropriate private key:
        # if i == 110000:
        #     priv_key = bytes.fromhex('60cf347dbc59d31c1358c8e5cf5e45b822ab85b79cb32a9f3d98184779a9efc2')

        publ_key = getPubKeyFaster(priv_key)

        # search public key uncompressed
        publ_key_uncompressed = getPubKeyFullUncompressedFaster(publ_key)
        hash160 = getPubKeyHashed(publ_key_uncompressed)
        searchInList(priv_key, hash160, hash160Set, 'uncompressed', foundFile)

        # search public key compressed
        publ_key_compressed = getPubKeyFullCompressedFaster(publ_key)
        hash160 = getPubKeyHashed(publ_key_compressed)
        searchInList(priv_key, hash160, hash160Set, 'compressed', foundFile)

        time_diff = dt.datetime.today().timestamp() - start_time
        if (i % LOG_EVERY_N) == 0:
            threadSpeed = i / time_diff
            setSize = len(hash160Set)
            yearsLeft = yearsToFindAkey(threadSpeed, threads, setSize)
            print("Thread: %s | priv keys/s = %s | matches G/s: %s | priv keys processed: %s | elapsed s %s | years to find a key %s" % (thread, format(i / time_diff, '.2f'), format(i * setSize * 2 / 1000000000 / time_diff, '.2f'), i, format(time_diff, '.1f'), yearsLeft))


if __name__ == '__main__':
    jobs = []
    hash160Set = createHashedPubKeySetFromAddressList(addressFile)
    print('File %s loaded, number of unique addresses: %s' % (addressFile, len(hash160Set)))
    for thread in range(threads):
        p = multiprocessing.Process(target=seek, args=(thread,hash160Set))
        jobs.append(p)
        p.start()

