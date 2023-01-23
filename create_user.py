from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import load_pem_private_key


KEY_STORAGE_FILE = "mykeys"

class KeyPair:
    """
    Holds the private key objects, and has a collection of methods
    for creating and loading key pairs. Serialization adopted from 
    https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b
    """
    def __init__(self, private_key) -> None:
        self.private_key = private_key

    @staticmethod
    def load_key_pair(fileName=KEY_STORAGE_FILE):
        """
        Reads the key storage file located in the same directory as this module,
        and returns a new KeyPair object containing the loaded keys.
        """
        with open(fileName, 'rb') as pem_in:
            pem_content = pem_in.read()
        password = input("Enter password below:\n")
        private_key = load_pem_private_key(pem_content, password.encode('utf-8'), default_backend())
        return KeyPair(private_key)
    
    @staticmethod
    def create_new_key_pair(fileName=KEY_STORAGE_FILE):
        """
        Creates a new pair of keys for encryption, saves them into the key storage file,
        and returns a KeyPair object containing the newly created keys.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Get a password with which to encrypt and save the private key
        password = "x"
        re_entered = ""
        while password != re_entered or not password:
            password = input("Enter password below:\n")
            re_entered = input("Confirm password below:\n")
        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )
        with open(fileName, 'wb') as private_key_store:
            private_key_store.write(encrypted_pem_private_key)

        # TODO: Figure out why I don't need to save the public key (which still gets accessible somehow)

        return KeyPair(private_key)
