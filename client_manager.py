from key_pair import KeyPair, KEY_STORAGE_FILE
from event import BaseEvent, TextEvent
import json
import asyncio
import websockets

class ClientMessageType():
    EVENT = "EVENT"
    REQUEST = "REQ"
    CLOSE = "CLOSE"

RELAY_FILE = "myrelays"

class ClientManager:
    def __init__(self, keys, relays=[], relay_file=RELAY_FILE) -> None:
        self.keys = keys
        self.relays = relays
        self.relay_file = relay_file

    def run_loop(self):
        while (True):
            print("What may I do for you sir? ('fetch', 'post', 'subscribe', 'info' or 'exit')")
            command = input(">")
            if not command:
                continue
            elif command[0] in ['e', 'E']:
                break
            elif command[0] in ['f', 'F']:
                # TODO: Fetch content from relay
                continue
            elif command[0] in ['p', 'P']:
                content = input("Enter content below:\n>")
                if not content: continue
                event = TextEvent(self.keys.hex_pub_key(), content)
                payload = self.get_event_payload(event)
                asyncio.get_event_loop().run_until_complete(self.publish_payload(payload))
            elif command[0] in ['s', 'S']:
                # TODO: Subscribe to some relay
                continue
            elif command[0] in ['i', 'I']:
                print("User:", self.keys.hex_pub_key())
    
    def get_event_payload(self, event):
        (timestamp, serialized_event) = event.stamped_event()
        id_of_event = BaseEvent.get_id_from_stamped_event(serialized_event)
        signature = self.keys.sign_bytes(bytes.fromhex(id_of_event))
        print("id", id_of_event)
        print("pubkey", event.author)
        print("created_at", timestamp)
        print("kind", event.get_kind())
        print("tags", event.tags)
        print("content", event.content)
        print("sig", signature)
        return json.dumps([
            ClientMessageType.EVENT,
            {
                "id": id_of_event,
                "pubkey": event.author,
                "created_at": timestamp,
                "kind": event.get_kind(),
                "tags": event.tags,
                "content": event.content,
                "sig": signature
            }
        ])

    async def publish_payload(self, payload):
        """
        Publish a payload to all relays.
        """
        if not self.relays:
            return Exception("No relays to publish to.")
        for relay in self.relays:
            async with websockets.connect(relay) as connection:
                await connection.send(payload)
                response = await connection.recv()
                print(response)

    @staticmethod
    def initialize():
        print("Hello sir!")
        keys = ClientManager.get_user_keys()
        relays = ClientManager.get_relays()
        client = ClientManager(keys, relays)
        client.run_loop()

    @staticmethod
    def get_user_keys():
        print(f"Would you like to load user keys from '{KEY_STORAGE_FILE}'? ('yes'/'no')")
        load_new_user = input(">")
        if load_new_user and load_new_user[0] in ['y', 'Y']:
            keys = KeyPair.load_key_pair(KEY_STORAGE_FILE)
        else:
            target_file = None
            print("Would you like to create a new default user? ('yes'/'no')")
            create_default_user = input(">")
            if create_default_user and create_default_user[0] in ['y', 'Y']:
                target_file = KEY_STORAGE_FILE
            else:
                timestamp = str(time.time())
                target_file = "mykeys_" + timestamp
            keys = KeyPair.create_new_key_pair()
            keys.save_key(target_file)
        return keys

    def add_new_relay(self, relay):
        self.relays.append(relay)

    @staticmethod
    def get_relays():
        print(f"Would you like to load relay list from '{RELAY_FILE}'? ('yes'/'no')")
        load_relay = input(">")
        if load_relay and load_relay[0] in ['y', 'Y']:
            relays = ClientManager.load_relays(RELAY_FILE)
        else:
            relays = input("Enter a comma-separated list of relays below:\n>")
            relays = relays.split(",")
            target = input(f"Would you like to save this list? (Hit enter to save to {RELAY_FILE}.)")
            if not target: target = RELAY_FILE
            ClientManager.save_relays(relays, target)
        return relays

    @staticmethod
    def save_relays(relays, file_name=RELAY_FILE):
        with open(file_name, "w") as f:
            for relay in relays:
                f.write(relay + "\n")
            f.close()
    
    @staticmethod
    def load_relays(file_name=RELAY_FILE):
        relays = []
        with open(file_name, "r") as f:
            for line in f:
                relays.append(line.strip())
            f.close()
        return relays