#> =============================================================================
#>                     This confidential and proprietary code
#>                       may be used only as authorized by a
#>                         licensing agreement from
#>                     KU Leuven, ESAT Department, COSIC Group
#>                    https://securewww.esat.kuleuven.be/cosic/
#>                        _____  ____    ____   ____  _____
#>                       / ___/ / __ \  / __/  /  _/ / ___/
#>                      / /__  / /_/ / _\ \   _/ /  / /__
#>                      \___/  \____/ /___/  /___/  \___/
#>
#>                              ALL RIGHTS RESERVED
#>        The entire notice above must be reproduced on all authorized copies.
#> =============================================================================
#> File name     : EagleCrypt.py
#> Time created  : Fri Sep 14 12:03:43 2018
#> Author        : dsijacic (dsijacic@esat.kuleuven.be)
#> Details       :
#>               :
#> =============================================================================


import ctypes

KeySizeInBits = 96
NonceSizeInBits = 80
TagSizeInBits = 40

# HW or SW depending on the type of acceleration
CRYPTO_TYPE = "SW"

class CryptoException(Exception):
    """ Custom exception class for the crypto operations. """
    def __init__(self):
        super(CryptoException, self).__init__('Crypto operation failed.')

# platform dependent configuration (choose the right shared libraries)
if CRYPTO_TYPE == "SW":
    _crypto = ctypes.CDLL("libcryptosw.so")
else:
    _crypto = ctypes.CDLL("libcryptohw.so")

_crypto.hash.argtypes = (
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint
)

_crypto.encrypt.argtypes = (
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint
)

_crypto.decrypt.argtypes = (
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint,
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.POINTER(ctypes.c_ubyte),
    ctypes.c_uint
)

def hash(dataBytes, digestByteLen):
    global _crypto

    dataByteLen = len(dataBytes)

    digest = (ctypes.c_ubyte * digestByteLen)()

    result = _crypto.hash(
        (ctypes.c_ubyte * dataByteLen)(*dataBytes),
        ctypes.c_uint(dataByteLen),
        digest,
        ctypes.c_uint(digestByteLen)
    )

    result = int(result)
    if result != 0:
        raise CryptoException()

    digest = bytearray(digest)

    return digest

def encrypt(keyBytes, nonceBytes, adBytes, ptBytes, tagByteLen):

    ct = (ctypes.c_ubyte * (len(ptBytes)))()
    tag = (ctypes.c_ubyte * tagByteLen)()

    result = _crypto.encrypt(
        (ctypes.c_ubyte * len(keyBytes))(*keyBytes), ctypes.c_uint(len(keyBytes)),
        (ctypes.c_ubyte * len(nonceBytes))(*nonceBytes), ctypes.c_uint(len(nonceBytes)),
        (ctypes.c_ubyte * len(adBytes))(*adBytes), ctypes.c_uint(len(adBytes)),
        (ctypes.c_ubyte * len(ptBytes))(*ptBytes), ctypes.c_uint(len(ptBytes)),
        ct,
        tag, ctypes.c_uint(tagByteLen)
    )

    if result != 0:
        raise CryptoException()
    ct = bytearray(ct)
    tag = bytearray(tag)
    return ct, tag

def decrypt(keyBytes, nonceBytes, adBytes, ctBytes, tagBytes):

    pt = (ctypes.c_ubyte * (len(ctBytes)))()
    tag = (ctypes.c_ubyte * (len(tagBytes)))()

    result = _crypto.decrypt(
        (ctypes.c_ubyte * len(keyBytes))(*keyBytes), ctypes.c_uint(len(keyBytes)),
        (ctypes.c_ubyte * len(nonceBytes))(*nonceBytes), ctypes.c_uint(len(nonceBytes)),
        (ctypes.c_ubyte * len(adBytes))(*adBytes), ctypes.c_uint(len(adBytes)),
        (ctypes.c_ubyte * len(ctBytes))(*ctBytes), ctypes.c_uint(len(ctBytes)),
        pt,
        tag, ctypes.c_uint(len(tagBytes))
    )

    if result != 0:
        raise CryptoException()

    tag = bytearray(tag)
    if tag == tagBytes:
        pt = bytearray(pt)
    else:
        pt = bytearray()

    return pt

if __name__ == '__main__':

    from utils import *
    from random import randint

    for i in range(0xff):
        if (i>0 and not i % 100): print(i)
        key = bytearray([randint(0, 255) for _ in range(KeySizeInBits//8)])
        ad = bytearray([randint(0, 255) for _ in range(randint(0, 1024))])
        pt = bytearray([randint(0, 255) for _ in range(randint(0, 1024))])
        nonce = bytearray([randint(0, 255) for _ in range(NonceSizeInBits//8)])

        ct, tag = encrypt(key, nonce, ad, pt, TagSizeInBits//8)
        pt_new = decrypt(key, nonce, ad, ct, tag)
        if i < 1:
            ppBytes(pt, label='pt src')
            ppBytes(ad, label='ad')
            ppBytes(ct, label='ct')
            ppBytes(tag, label='tag')
            ppBytes(pt_new, label='pt dst')

        assert pt == pt_new
    print('success!')
