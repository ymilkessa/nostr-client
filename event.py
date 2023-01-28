from enum import Enum
import time
import json

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

    def add_tag(self, new_tag):
        self.tags.append(new_tag)

    def stamped_event(self):
        """
        Serializes the event by also adding a timestamp. All contents 
        before the serialization are expected to be composed of ascii characters.
        Non-ascii characters are ignored. To include them, add ensure_ascii=True flag
        in the call to json.dump()
        """
        timestamp = int(time.time())
        base_array = [0, self.author, timestamp, self.kind.value, self.tags, self.content]
        str_format = json.dump(base_array, separators=(',', ':'))
        return str_format.encode()
