from errors import FileNonExistentError
from base_interface import BaseInterface

from config import UserConfig, RELAY_FILE_KEY

class Relays:
    def __init__(self, relay_file, interface=BaseInterface()) -> None:
        self.relay_urls = []
        self.relay_file = relay_file
        self.interface = interface

        self.load_relays_from_file()

    def add_new_relays(self, relays: "list[str]"):
        if not relays: return
        self.relay_urls += relays
        if not self.relay_file:
            print(FileNonExistentError.note)
        else:
            self.save_relays()

    def get_new_relays(self):
        relays = self.interface.get_comma_sep_list("relay URLs")
        if not relays:
            print("No relays were added.")
            return
        self.relay_urls += relays.split(",")
        self.save_relays()

    def set_new_relay_file(self, file_name):
        if not file_name:
            return ValueError("No file name given.")
        self.relay_file = file_name
        # Create relay file if it doesn't exist. Read it if it does.
        try:
            with open(self.relay_file, "r") as f:
                new_relays = []
                for line in f:
                    new_relays.append(line.strip())
                self.relay_urls = new_relays
                f.close()
        except FileNotFoundError:
            with open(self.relay_file, "w") as f:
                f.close()
            self.relay_urls = []

    def save_relays(self):
        with open(self.relay_file, "w") as f:
            f.write("\n".join(self.relay_urls))
            f.close()
    
    def load_relays_from_file(self):
        set_of_relays = set(self.relay_urls)
        with open(self.relay_file, "r") as f:
            lines = f.readlines()
            f.close()
        if not lines:
            print("No relays found in relay file.")
            return
        for line in lines:
            set_of_relays.add(line.strip())
        self.relay_urls = list(set_of_relays)
    
    @staticmethod
    def get_relays(configs=UserConfig(), interface=BaseInterface()):
        file_name = configs.get_client_config(RELAY_FILE_KEY)
        return Relays(file_name, interface)
