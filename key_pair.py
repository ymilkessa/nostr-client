import os
import secrets

import secp256k1
import hashlib
from base64 import b64encode
from cryptography.fernet import Fernet


KEY_STORAGE_FILE = "mykeys"


class KeyPair:
    """
    Holds the private key objects, and has a collection of methods
    for creating and loading key pairs.
    """

    def __init__(self, private_key, key_store_file=None) -> None:
        self.private_key = private_key
        self.key_store_file = key_store_file

    def private_key_bytes(self):
        return self.private_key.private_key

    def public_key_bytes(self):
        # Ignore the "sign byte" of the ECC public key, as per https://bips.xyz/340#public-key-generation
        return self.private_key.pubkey.serialize()[1:]

    def hex_pub_key(self):
        pubkey = self.public_key_bytes()
        return pubkey.hex()
    
    def hex_priv_key(self):
        priv_key = self.private_key_bytes()
        return priv_key.hex()

    def delete_key_file(self):
        os.remove(self.key_store_file)
    
    def sign(self, content):
        """
        Returns the singature for the content
        """
        return self.priv_key.schnorr_sign(content)

    def verify_signature(self, content, signature):
        return self.private_key.schnorr_verify(content, signature)
    
    def save_key(self, file_name=KEY_STORAGE_FILE, set_key_store=True):
        """
        Encrypts and saves the private key to a file.
        """
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
        encrypted_key = f.encrypt(self.private_key_bytes())
        with open(file_name, 'wb') as storage_file:
            storage_file.write(encrypted_key)
        if set_key_store:
            self.key_store_file = file_name

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
    def create_new_key_pair():
        """
        Creates a new valid key pair using the secp256k1 curve and saves it to a file.
        Essentially creates the keys for a new Nostr user.
        """
        secret_bytes = secrets.token_bytes(32)
        priv_key = secp256k1.PrivateKey(secret_bytes, raw=True)

        return KeyPair(priv_key)
