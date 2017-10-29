#!/bin/bash

set -e

echo 'Keys and GnuPG home will be created in the current path.'
mkdir -p -m700 $(pwd)/gnupg
export GNUPGHOME=$(pwd)/gnupg
EMAIL=cv25519@test.key
FILE=plain.txt
echo '1. generate EC & EC gpg key par'
gpg --quick-generate-key --batch  --passphrase '' $EMAIL future-default default
# show the key info
# gpg --with-colons --with-key-data --list-keys
echo '2. export the secret key, no armor!'
gpg --export-secret-key $EMAIL > $EMAIL.sec
echo '3. "split" the secret key'
mkdir $EMAIL.sec.d
mv $EMAIL.sec $EMAIL.sec.d
cd $EMAIL.sec.d
gpgsplit $EMAIL.sec
ls
echo '000004-007.secret_subkey is the secret subkey packet'
echo '4. encrypt a file, no armor!'
cd ..
echo 'foo' > $FILE
gpg --encrypt -r $EMAIL $FILE
# show PKESK
# gpg --decrypt --show-session-key < $FILE.gpg
echo '5. "split" the encrypted file'
mkdir $FILE.gpg.d
mv $FILE.gpg $FILE.gpg.d
cd $FILE.gpg.d
gpgsplit $FILE.gpg
ls
echo '000001-001.pk_enc is the session key packet encrypted with the public key'
cd ..

echo '6. Decrypt the encrypted session key'
./decrypt_seskey.py $FILE.gpg.d/000001-001.pk_enc $EMAIL.sec.d/000004-007.secret_subkey
