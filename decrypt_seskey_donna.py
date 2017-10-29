#!/usr/bin/env python3
"""Example script to decrypt an OpenPGP encrypted session key packet
with the secret key packet."""

import codecs
import logging
import sys

from pgpy import pgp
import donna25519


__help__ = """Example script to decrypt an OpenPGP encrypted session key packet
with the secret key packet.
arg1: encrypted session key packet (PKESK).
arg2: secret key packet.
Output: decrypted session key packet."""

# logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def dec_seskey_with_donna(pkeskfp, seckeypktfp):
    with open(seckeypktfp, 'rb') as f:
        seckeypkt = pgp.Packet(bytearray(f.read()))
    with open(pkeskfp, 'rb') as f:
        pkesk = pgp.Packet(bytearray(f.read()))
    pubkey = donna25519.PublicKey(bytes(pkesk.ct.vX))
    # pubkey = donna25519.PublicKey(bytes(pkesk.ct.compressed))
    seckey = donna25519.PrivateKey.load(
        seckeypkt.keymaterial.s.to_bytes(32, 'little'))
    seskey = seckey.do_exchange(pubkey)
    return seskey


if __name__ == '__main__':
    print(__help__)
    seskeydonna = dec_seskey_with_donna(sys.argv[1], sys.argv[2])
    print('Session key donna {}'.format(seskeydonna))
