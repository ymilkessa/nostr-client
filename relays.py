RELAY_FILE = "myrelays"
from errors import FileNonExistentError
from base_interface import BaseInterface

class Relays:
    def __init__(self, relay_file=None, interface=BaseInterface()) -> None:
        self.relay_urls = []
        self.relay_file = None
        self.interface = interface

        if not relay_file:
            relay_file = self.interface.get_input("Enter the name for a relay file you wish to use/create? (Hit enter to use the default '{RELAY_FILE}' file.)\n>")
            relay_file = relay_file or RELAY_FILE
        self.set_relay_file(relay_file)
        self.load_relays_from_file()

    def add_new_relays(self, relays: "list[str]"):
        if not relays: return
        self.relay_urls += relays
        if not self.relay_file:
            print(FileNonExistentError.note)
        else:
            self.save_relays()

    def get_new_relays(self):
        relays = self.interface.get_input("Enter a comma-separated list of relays below:\n>")
        if not relays:
            print("No relays were added.")
            return
        self.relay_urls += relays.split(",")
        self.save_relays()

    def set_relay_file(self, file_name):
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
        if not self.relay_file:
            return FileNonExistentError("relay file")
        with open(self.relay_file, "w") as f:
            for relay in self.relay_urls:
                f.write(relay + "\n")
            f.close()
    
    def load_relays_from_file(self):
        if not self.relay_file:
            return FileNonExistentError("relay file")
        set_of_relays = set(self.relay_urls)
        with open(self.relay_file, "r") as f:
            for line in f:
                set_of_relays.add(line.strip())
            f.close()
            self.relay_urls = list(set_of_relays)
