import unittest
from unittest.mock import patch

import sys
sys.path.append("src")

from key_pair import KeyPair


class KeyPairTests(unittest.TestCase):

    def setUp(self) -> None:
        self.key_pair = KeyPair.create_new_key_pair()

    def tearDown(self) -> None:
        return super().doCleanups()

    def test_key_loading(self):
        test_file_name = "mykeys_test_loading"
        password = "test123"
        with unittest.mock.patch("base_interface.BaseInterface.get_password", return_value=password):
            self.key_pair.save_key(test_file_name)
        public_key_str = self.key_pair.pubkey_hex_string()

        # Now load the keys from file by patching how the password is retrieved.
        with unittest.mock.patch("base_interface.BaseInterface.get_password", return_value=password):
            loaded_keys = KeyPair.load_key_pair(test_file_name)
        loaded_public_key = loaded_keys.pubkey_hex_string()

        # Ensure that the created keys are the same as the loaded keys.
        self.assertEqual(public_key_str, loaded_public_key)
        self.key_pair.delete_key_file()
    
    def test_signature(self):
        content = b"Hello world, this is a test message."
        signature = self.key_pair.sign_bytes(content)
        verification_res = self.key_pair.verify_signature(content.hex(), signature)
        self.assertEqual(verification_res, True)

if __name__ == '__main__':
    unittest.main()
