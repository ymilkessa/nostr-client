import unittest
from event import BaseEvent, EventKinds

class EventTests(unittest.TestCase):
    def setUp(self):
        author = "".join(random.choices('0123456789abcdef', k=64))
        author_pub_key = bytes.fromhex(author)
        content = b"Hello there"     
        self.event = BaseEvent(author_pub_key, content, EventKinds.TEXT_NOTE)
