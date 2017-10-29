#!/usr/bin/env python3
"""Example script to decrypt an OpenPGP encrypted session key packet
with the secret key packet."""

import codecs
import sys

from pgpy import pgp


__help__ = """Example script to decrypt an OpenPGP encrypted session key packet
with the secret key packet.
arg1: encrypted session key packet (PKESK).
arg2: secret key packet.
Output: decrypted session key packet."""


def seskey2str(seskey):
    return str(int(seskey[0])) + ":" + \
           codecs.decode(codecs.encode(seskey[1], 'hex')).upper()


def dec_seskey(pkeskfp, seckeypktfp):
    with open(seckeypktfp, 'rb') as f:
        seckeypkt = pgp.Packet(bytearray(f.read()))
    with open(pkeskfp, 'rb') as f:
        pkesk = pgp.Packet(bytearray(f.read()))
    seskey = pkesk.decrypt_sk(seckeypkt)
    return seskey


if __name__ == '__main__':
    print(__help__)
    seskey = dec_seskey(sys.argv[1], sys.argv[2])
    print('Session key encoded string: {}'.format(seskey2str(seskey)))
