import unittest
from unittest.mock import patch

from key_pair import KeyPair


class KeyPairTests(unittest.TestCase):

    def setUp(self) -> None:
        self.key_store_file = "mykeys_test"
        self.password = "test123"
        key_pair = KeyPair.create_new_key_pair()
        with patch('builtins.input', return_value=self.password):
            key_pair.save_key(self.key_store_file)

    def tearDown(self) -> None:
        with patch('builtins.input', return_value=self.password):
            loaded_keys = KeyPair.load_key_pair(self.key_store_file)
        loaded_keys.delete_key_file()
        return super().doCleanups()

    def test_key_loading(self):
        test_file_name = "mykeys_test_loading"
        key_pair = KeyPair.create_new_key_pair()
        with patch('builtins.input', return_value=self.password):
            key_pair.save_key(test_file_name)
        private_key_str = key_pair.hex_priv_key()
        public_key_str = key_pair.hex_pub_key()

        # Now load the keys from file
        with patch('builtins.input', return_value=self.password):
            loaded_keys = KeyPair.load_key_pair(test_file_name)
        loaded_private_key = loaded_keys.hex_priv_key()
        loaded_public_key = loaded_keys.hex_pub_key()
        
        # Ensure that the created keys are the same as the loaded keys.
        self.assertEqual(private_key_str, loaded_private_key)
        self.assertEqual(public_key_str, loaded_public_key)
        key_pair.delete_key_file()

if __name__ == '__main__':
    unittest.main()
