import os, binascii

def hex_random(num_bytes):
    return binascii.b2a_hex(os.urandom(num_bytes))

DEBUG=True # True => Security Hole
VIDEO_JSON="videos.json"

COOKIE_KEY='0753e9465b8e5d2a0391dc3ef3f2e9a6ca14fc1bed63eae2c2101af80412de19c82553d532839495cc2b9e5db512d543dfb12cdbf9530c68fe9c57ced074c97a'
SECRET_KEY='development key'
