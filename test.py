import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import secp256k1

from key_pair import KeyPair


class KeyPairTests(unittest.TestCase):

    def setUp(self) -> None:
        self.key_store_file = "mykeys_test"
        self.password = "test123"
        with patch('builtins.input', return_value=self.password):
            key_pair = KeyPair.create_new_key_pair(self.key_store_file)

    def tearDown(self) -> None:
        with patch('builtins.input', return_value=self.password):
            loaded_keys = KeyPair.load_key_pair(self.key_store_file)
        loaded_keys.delete_key_file()
        return super().doCleanups()

    def test_key_loading(self):
        test_file_name = "mykeys_test_loading"
        with patch('builtins.input', return_value=self.password):
            key_pair = KeyPair.create_new_key_pair(test_file_name)
        private_key_str = key_pair.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_str = key_pair.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Now load the keys from file
        with patch('builtins.input', return_value=self.password):
            loaded_keys = KeyPair.load_key_pair(test_file_name)
        loaded_private_key = key_pair.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        loaded_public_key = loaded_keys.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        # Ensure that the created keys are the same as the loaded keys.
        self.assertEqual(private_key_str, loaded_private_key)
        self.assertEqual(public_key_str, loaded_public_key)
        key_pair.delete_key_file()

    # def test_hex_format(self):
    #     with patch('builtins.input', return_value=self.password):
    #         loaded_keys = KeyPair.load_key_pair(self.key_store_file)
    #     public_key_bytes = loaded_keys.private_key.public_key().public_bytes(
    #         encoding=serialization.Encoding.DER, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    #     hex_string = public_key_bytes.hex()
    #     print(hex_string)
    #     print("\n\n")
    #     pk_new = secp256k1.PublicKey(b"\x02" + public_key_bytes, True)
    #     print(pk_new.hex())


if __name__ == '__main__':
    unittest.main()
