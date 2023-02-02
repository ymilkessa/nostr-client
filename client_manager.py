# import asyncio
import json
import time
from hashlib import sha256
from threading import Thread

from websocket import create_connection

from base_interface import BaseInterface
from constants import ClientMessageType
from event import BaseEvent, TextEvent
from key_pair import KEY_STORAGE_FILE, KeyPair
from relays import RELAY_FILE, Relays
from request import Request


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
                event = TextEvent(self.keys.pubkey_hex_string(), content)
                payload = self.get_event_payload(event)
                self.publish_payload(payload)
                
            elif command[0] in ['s', 'S']:
                # TODO Setup a better subscription feature
                payload = self.get_subscription_payload()
                self.publish_payload(payload)
                time.sleep(1.5)
            elif command[0] in ['i', 'I']:
                print("User public key:", self.keys.pubkey_hex_string())
                words = command.split(" ")
                if len(words) > 1 and words[1] in ['-a', '--all']:
                        print("User private key:", self.keys.privkey_hex_string())
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

    def get_subscription_payload(self):
        target_pubkey = self.interface.get_input("Enter the public key of the user you want to subscribe to: \n>")
        if not target_pubkey:
            return ""
        my_pubkey = self.keys.pubkey_hex_string()
        subscription_id = sha256((my_pubkey + " follows " + target_pubkey).encode('utf-8')).hexdigest()
        return json.dumps([ClientMessageType.REQUEST, subscription_id, {
            "authors": [target_pubkey]
        }])

    def publish_payload(self, payload):
        """
        Publish a payload to all relays.
        """
        if not self.relays.relay_urls:
            return Exception("No relays to publish to.")
        threads = []
        for relay in self.relays.relay_urls:
            # Send out each message in a separate thread
            t = Thread(target=self.publish_to_relay, args=(relay, payload))
            threads.append(t)
            t.start()

        # Wait for 2.5 seconds and then end the still running threads.
        time.sleep(2.5)
        for t in threads: 
            if t.is_alive():
                t.raise_exception()
            t.join()

    def publish_to_relay(self, relay_url, payload):
        try:
            ws = create_connection(relay_url)
            ws.send(payload)
            response = ws.recv()
            print(f"Response from {relay_url}:", response)
            ws.close()
        except:
            print(f"Failed to publish to {relay_url}.")

    @staticmethod
    def initialize_saved_user():
        print("Hello sir!")
        client = ClientManager()
        client.run_loop()

if __name__ == "__main__":
    ClientManager.initialize_saved_user()
