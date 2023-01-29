from key_pair import KeyPair, KEY_STORAGE_FILE
import time

class ClientManager:
    def __init__(self, keys):
        self.keys = keys

    def run_loop(self):
        while (True):
            print("What may I do for you sir? ('fetch', 'post', 'subscribe' or 'exit')\n")
            command = input(">")
            if not command:
                continue
            elif command[0] in ['e', 'E']:
                break
            elif command[0] in ['f', 'F']:
                # TODO: Fetch content from relay
                continue
            elif command[0] in ['p', 'P']:
                # TODO: Begin post sequence
                continue
            elif command[0] in ['s', 'S']:
                # TODO: Subscribe to some relay
                continue

    @staticmethod
    def initialize():
        print("Hello sir!\n")
        print(f"Would you like to load user keys from '{KEY_STORAGE_FILE}'? ('yes'/'no')\n")
        load_new_user = input(">")
        if load_new_user and load_new_user[0] in ['y', 'Y']:
            client = ClientManager.load_user()
        else:
            target_file = None
            print("Would you like to create a new default user? ('yes'/'no')\n")
            create_default_user = input(">")
            if create_default_user and create_default_user[0] in ['y', 'Y']:
                target_file = KEY_STORAGE_FILE
            client = ClientManager.create_new_user(target_file)
        client.run_loop()

    @staticmethod
    def load_user(file_name=KEY_STORAGE_FILE):
        keys = KeyPair.load_key_pair(file_name)
        return ClientManager(keys)
    
    @staticmethod
    def create_new_user(file_name = None):
        keys = KeyPair.create_new_key_pair()
        if file_name is None:
            timestamp = str(time.time())
            file_name = "mykeys_" + timestamp
        keys.save_key(file_name)
        return ClientManager(keys)