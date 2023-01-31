import os
import secrets

import secp256k1
import hashlib
from base64 import b64encode
from cryptography.fernet import Fernet
from base_interface import BaseInterface

KEY_STORAGE_FILE = "mykeys"


class KeyPair:
    """
    Holds the private key objects, and has a collection of methods
    for creating and loading key pairs.
    """

    def __init__(self, private_key, key_store_file=None) -> None:
        self._private_key = private_key
        self.key_store_file = key_store_file

    def _private_key_bytes(self):
        return self._private_key.private_key

    def _public_key_bytes(self):
        # Ignore the "sign byte" of the ECC public key, as per https://bips.xyz/340#public-key-generation
        return self._private_key.pubkey.serialize()[1:]

    def pubkey_hex_string(self):
        """
        Returns the public key as a string of the hexadecimal characters

        Returns:
            str: hex string of public key
        """
        pubkey = self._public_key_bytes()
        return pubkey.hex()

    def delete_key_file(self):
        os.remove(self.key_store_file)
    
    def sign_bytes(self, msg):
        """
        Returns the singature for the message
        """
        signature_bytes = self._private_key.schnorr_sign(msg, None, raw=True)
        return signature_bytes.hex()

    def verify_signature(self, msg, signature):
        msg_bytes = bytes.fromhex(msg)
        signature_bytes = bytes.fromhex(signature)
        return self._private_key.pubkey.schnorr_verify(msg_bytes, signature_bytes, None, raw=True)
    
    def save_key(self, file_name=KEY_STORAGE_FILE, interface=BaseInterface(),set_key_store=True):
        """
        Encrypts and saves the private key to a file.
        """
        if not file_name:
            raise ValueError("File name must be provided.")

        # Get a password with which to encrypt and save the private key
        password = "x"
        re_entered = ""
        while password != re_entered or not password:
            password = interface.get_password("Enter password below\n>")
            re_entered = interface.get_password("Confirm password below:\n>")
        hash_str = hashlib.sha256(password.encode('utf-8')).hexdigest()
        hash_as_bytes = bytes.fromhex(hash_str)
        b64_version = b64encode(hash_as_bytes)
        f = Fernet(b64_version)

        # Now encrypt and save the key
        encrypted_key = f.encrypt(self._private_key_bytes())
        with open(file_name, 'wb') as storage_file:
            storage_file.write(encrypted_key)
        if set_key_store:
            self.key_store_file = file_name

    @staticmethod
    def get_user_keys(key_file=None, interface = BaseInterface()):
        if not key_file:
            file_name = interface.get_input(f"Enter a file name to save the keys to: (Hit enter to use '{KEY_STORAGE_FILE}') \n>")
            if not file_name: file_name = KEY_STORAGE_FILE
            keys = KeyPair.create_new_key_pair()
            keys.save_key(file_name, interface)
        else:
            keys = KeyPair.load_key_pair(key_file, interface)
        return keys

    @staticmethod
    def load_key_pair(file_name = KEY_STORAGE_FILE, interface = BaseInterface()):
        """
        Reads the key storage file located in the same directory as this module,
        and returns a new KeyPair object containing the loaded keys.
        """
        if file_name is None:
            file_name = KEY_STORAGE_FILE
        password = interface.get_password("Enter password below:\n>")
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
