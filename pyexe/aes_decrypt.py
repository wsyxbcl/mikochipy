#!/usr/bin/python

import sys
from Crypto.Cipher import AES

def decrypt(data, key, output, mode=AES.MODE_CBC):
    """
    decrypt AES encrypted video file
    """
    with open(key, 'rb') as fp:
        cipher = AES.new(fp.read(), mode)
    with open(data, 'rb') as fp:
        print("Decrypting...")
        content = cipher.decrypt(fp.read())
    with open(output, 'wb') as fp:
        print("Writing to {}".format(output))
        fp.write(content)

if __name__ == "__main__":
    try:
        path_data, path_key, path_output= sys.argv[1], sys.argv[2], sys.argv[3]
    except IndexError:
        print("Usage: aes_decrypt.py [input file] [key] [output file]")
        sys.exit(1)
    decrypt(data=path_data, key=path_key, output=path_output)
