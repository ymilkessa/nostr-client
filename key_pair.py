import os
import quantumrandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key

import secp256k1
import hashlib
from base64 import b64encode
from cryptography.fernet import Fernet


KEY_STORAGE_FILE = "mykeys"


class KeyPair:
    """
    Holds the private key objects, and has a collection of methods
    for creating and loading key pairs. Serialization adopted from 
    https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b
    """

    def __init__(self, private_key, key_store_file) -> None:
        self.private_key = private_key
        self.key_store_file = key_store_file

    def private_key_bytes(self):
        return self.private_key.private_key

    def public_key_bytes(self):
        # TODO: Figure out why this output is 33 bytes, and why the other repo simply ignores the first byte
        return self.private_key.pubkey.serialize()

    def hex_pub_key(self):
        pubkey = self.public_key_bytes()
        return pubkey.hex()
    
    def hex_priv_key(self):
        priv_key = self.private_key_bytes()
        return priv_key.hex()

    def delete_key_file(self):
        os.remove(self.key_store_file)
    
    @staticmethod
    def load_key_pair(file_name = KEY_STORAGE_FILE):
        """
        Reads the key storage file located in the same directory as this module,
        and returns a new KeyPair object containing the loaded keys.
        """
        password = input("Enter password below:\n")
        hash_str = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hash_as_bytes = bytes.fromhex(hash_str)
        b64_version = b64encode(hash_as_bytes)
        f = Fernet(b64_version)
        with open(file_name, 'rb') as key_file:
            key_content = key_file.read()
        secret_bytes = f.decrypt(key_content)
        priv_key = secp256k1.PrivateKey(secret_bytes, raw=True)
        return KeyPair(priv_key, file_name)

    @staticmethod
    def create_new_key_pair(file_name = KEY_STORAGE_FILE):
        """
        Creates a new valid key pair using the secp256k1 curve and saves it to a file.
        Essentially creates the keys for a new Nostr user.
        """
        try:
            qrng_result = quantumrandom.get_data(data_type='hex16', array_length=1, block_size=32)
        except:
            return Exception("Problem getting random number from QRNG API")
        secret_bytes = bytes.fromhex(qrng_result[0])
        priv_key = secp256k1.PrivateKey(secret_bytes, raw=True)

        # Get a password with which to encrypt and save the private key
        password = "x"
        re_entered = ""
        while password != re_entered or not password:
            password = input("Enter password below:\n")
            re_entered = input("Confirm password below:\n")
        hash_str = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hash_as_bytes = bytes.fromhex(hash_str)
        b64_version = b64encode(hash_as_bytes)
        f = Fernet(b64_version)

        # Now encrypt and save the key
        encrypted_key = f.encrypt(secret_bytes)
        with open(file_name, 'wb') as storage_file:
            storage_file.write(encrypted_key)

        return KeyPair(priv_key, file_name)
