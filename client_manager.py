from base_interface import BaseInterface
from key_pair import KeyPair, KEY_STORAGE_FILE
from event import BaseEvent, TextEvent
import json
# import asyncio
import websockets
import time
from relays import Relays, RELAY_FILE

class ClientMessageType():
    EVENT = "EVENT"
    REQUEST = "REQ"
    CLOSE = "CLOSE"


class ClientManager:
    def __init__(self, key_file=KEY_STORAGE_FILE, relay_file=RELAY_FILE) -> None:
        self.interface = BaseInterface()
        self.relays = Relays(relay_file, self.interface)
        self.keys = KeyPair.get_user_keys(key_file, self.interface)

    def run_loop(self):
        while (True):
            print("What may I do for you sir? ('fetch', 'post', 'subscribe', 'info', 'exit', or 'help')")
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
                self.publish_payload(payload)
                # Wait for 1.5 seconds so the payload gets published
                time.sleep(1.5)
                # asyncio.get_event_loop().run_until_complete()
            elif command[0] in ['s', 'S']:
                # TODO: Subscribe to some relay
                continue
            elif command[0] in ['i', 'I']:
                print("User:", self.keys.hex_pub_key())
            elif command[0] in ['h', 'H']:
                print("Commands: 'fetch', 'post', 'subscribe', 'info', 'exit', 'help', 'add_relays'")
            elif command[0] in ['a', 'A']:
                self.relays.get_new_relays()
    
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
        if not self.relays.relay_urls:
            return Exception("No relays to publish to.")
        for relay in self.relays.relay_urls:
            async with websockets.connect(relay) as connection:
                await connection.send(payload)
                response = await connection.recv()
                print(response)

    @staticmethod
    def initialize_saved_user():
        print("Hello sir!")
        client = ClientManager()
        client.run_loop()
