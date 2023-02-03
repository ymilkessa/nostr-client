import unittest
from relays import Relays
import os

class RelaysTests(unittest.TestCase):
    def setUp(self) -> None:
        # Define a test relay file
        self.test_relay_file = "myrelays_test"
        self.relays = Relays(self.test_relay_file)
        super().setUp()
    
    def tearDown(self) -> None:
        # Delete the test relay file
        os.remove(self.test_relay_file)
        return super().tearDown()
    
    def test_relays_initialization(self):
        """
        Test that get_relays() uses the relay file provided int the config parameter.
        """
        # Patch the global RELAY_FILE variable
        test_default_file = "myrelays_test_default"
        patcher = unittest.mock.patch("config.UserConfig.get_client_config", test_default_file)
        patcher.start()
        relays = Relays.get_relays()
        patcher.stop()

        # Ensure that the mock relay file was used
        self.assertEqual(relays.relay_file, test_default_file)
        # Ensure that the test relay file was created
        self.assertTrue(os.path.exists(os.path.abspath(test_default_file)))
        os.remove(test_default_file)
        
    def test_get_new_relays(self):
        """
        get_new_relays() should save the relay urls provided via standard input
        """
        # first set a new relay file
        test_relay_file = "myrelays_test_get_new_relays"
        relays = Relays(test_relay_file)
        # Patch the BaseInterface.get_input() function to return a list of relay urls
        test_relays = ["relay1", "relay2", "relay3"]
        with unittest.mock.patch("base_interface.BaseInterface.get_input", return_value=",".join(test_relays)):
            relays.get_new_relays()
        # Ensure that the relay file contains the same relay urls as the ones provided
        with open(test_relay_file, "r") as f:
            relay_urls = f.read().splitlines()
        for relay in test_relays:
            self.assertIn(relay, relay_urls)
        os.remove(test_relay_file)

    def test_no_input_for_get_new_relays(self):
        """
        If no relays are entered via standard input, no relays should be added.
        """
        # first set a new relay file
        test_relay_file = "myrelays_no_relays_entered"
        relays = Relays(test_relay_file)
        # Patch the BaseInterface.get_input() function to return an empty string
        with unittest.mock.patch("base_interface.BaseInterface.get_input", return_value=""):
            relays.get_new_relays()
        # Ensure that the relay file is empty
        with open(test_relay_file, "r") as f:
            relay_urls = f.read().splitlines()
        self.assertEqual(relay_urls, [])
        os.remove(test_relay_file)

    def test_set_relay_file_updates_relay_urls(self):
        """
        When the relay_file is changed, the relay_urls attribute should be replaced by the 
        urls in the new relay file.
        """
        # first set a new relay file
        test_relay_file = "myrelays_test_relay_url_updates"
        test_relays = ["relay1", "relay2"]
        # Write these relays one per line in the relay file
        with open(test_relay_file, "w") as f:
            f.write("\n".join(test_relays))

        relays = Relays(test_relay_file)

        # Ensure that the relay_urls are correctly loaded from the relay file
        for relay in test_relays:
            self.assertIn(relay, relays.relay_urls)
        
        # Now set a new relay file
        test_relay_file_2 = "myrelays_test_relay_url_updates_2"
        test_relays_2 = ["relay3", "relay4"]
        with open(test_relay_file_2, "w") as f:
            f.write("\n".join(test_relays_2))
        
        # Now run set_relay_file() on 'relays' and check the change to the relay_urls
        relays.set_relay_file(test_relay_file_2)
        for relay in test_relays_2: 
            self.assertIn(relay, relays.relay_urls)
        for relay in test_relays:
            self.assertNotIn(relay, relays.relay_urls)

        os.remove(test_relay_file)
        os.remove(test_relay_file_2)
    
    def test_load_relays_from_file(self):
        """
        The relay_urls attribute should be populated with the urls in the relay file.
        """
        # first set a new relay file
        test_relay_file = "myrelays_test_load_relays"
        test_relays = ["relay1", "relay2"]
        # Write these relays one per line in the relay file
        with open(test_relay_file, "w") as f:
            f.write("\n".join(test_relays))

        relays = Relays(test_relay_file)

        # Ensure that the relay_urls are correctly loaded from the relay file
        for relay in test_relays:
            self.assertIn(relay, relays.relay_urls)
        
        # Now append a new relay to the file and run load_relays_from_file()
        new_relay = "relay3"
        with open(test_relay_file, "a") as f:
            f.write("\n" + new_relay)
        relays.load_relays_from_file()
        # Ensure that the new relay was added to the relay_urls
        self.assertIn(new_relay, relays.relay_urls)
        os.remove(test_relay_file)
