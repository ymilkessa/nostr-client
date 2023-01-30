from enum import Enum
import json
import time
from hashlib import sha256

class EventKinds(Enum):
    SET_METADATA = 0
    TEXT_NOTE = 1
    RECOMMEND_SERVER = 2


class BaseEvent:
    """
    Manages the events class of Nostr messages, which 
    is content to be published by clients along with associated metadata
    """
    def __init__(self, author, content, kind):
        """
        Setup an event instance with the given author and message.

        Args:
            author (str): the hexadecimal public key of the author
            message (str): the message to be posted in a string format
        """
        self.author = author
        self.content = content
        self.kind = kind
        self.tags = []

    def get_kind(self):
        return self.kind.value

    def tag_event(self, event_id, relay_url=""):
        """
        Tags another event of the given id onto this event.

        Args:
            event_id (bytes): 32-byte hex of the id
            relay_url (str, optional): Recommended relay url. Defaults to "".
        """
        self.tags.append(["e", event_id, relay_url])
    
    def tag_user(self, pub_key, relay_url=""):
        """
        Tags a user with the given public key onto this event.

        Args:
            pub_key (bytes): 32-byte hex of the user's public key
            relay_url (str, optional): Recommended relay url. Defaults to "".
        """
        self.tags.append(["p", pub_key, relay_url])
    
    def clear_tags(self):
        self.tags = []

    def stamped_event(self):
        """
        Serializes the event by also adding a timestamp. All contents 
        before the serialization are expected to be composed of ascii characters.
        Non-ascii characters are ignored. To include them, add ensure_ascii=True flag
        in the call to json.dumps()
        """
        timestamp = int(time.time())
        base_array = (timestamp, [0, self.author, timestamp, self.get_kind(), self.tags, self.content])
        str_format = json.dumps(base_array, separators=(',', ':'))
        return (timestamp, str_format.encode())
    
    @staticmethod
    def get_id_from_stamped_event(stamped_event):
        """
        Returns the sha256 hash of the input bytes as a bytes array.

        Args:
            stamped_event (bytes): bytes array of a serialized event, as per the nostr format

        Returns:
            bytes: 
        """
        hash_value = sha256(stamped_event)
        return hash_value.hexdigest()


class TextEvent(BaseEvent):
    """
    Manages simple text messages to be published by the client
    """
    def __init__(self, author, content):
        super().__init__(author, content, EventKinds.TEXT_NOTE)
