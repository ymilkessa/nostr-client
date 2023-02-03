from hashlib import sha256
import json
from constants import ClientMessageType
from base_interface import BaseInterface

class Request:
    def __init__(self, subscriber_id, subscription_params):
        
        self.subscription_params = subscription_params
        self.subscription_id = Request.get_subscription_id(subscriber_id, subscription_params)
    
    def start_subscription_payload(self):
        return json.dumps([ClientMessageType.REQUEST, self.subscription_id, self.subscription_params])
    
    def stop_subscription_payload(self):
        return json.dumps([ClientMessageType.CLOSE, self.subscription_id])

    @staticmethod
    def get_subscription_id(subscriber_id, subscription_params):
        serialized_string = subscriber_id + json.dumps(subscription_params)
        return sha256(serialized_string.encode('utf-8')).hexdigest()

    @staticmethod
    def setup_subscription_from_input(subscriber_id, interface=BaseInterface()):
        """
        Get the parameters of a subscription from user input and return the resulting
        Request object.
        """
        subscription_params = {}

        list_param_definitions = [
            ("public keys of authors", "authors"),
            ("event ids", "ids"),
            ("event kinds", "kinds"),
            ("referenced event ids", "#e"),
            ("referenced authors", "#p"),
        ]
        single_item_param_definitions = [
            ("Enter the oldest timestamp of events to fetch (in seconds since epoch):\n>", "since"),
            ("Enter the newest timestamp of events to fetch (in seconds since epoch):\n>", "until"),
            ("Enter the maximum number of events to fetch:\n>", "limit"),
        ]

        for item_name, item_key in list_param_definitions:
            list_input = interface.get_comma_sep_list(item_name)
            if list_input:
                subscription_params[item_key] = list_input
        
        for prompt, param_key in single_item_param_definitions:
            input = interface.get_input(prompt)
            if input:
                subscription_params[param_key] = input
        
        return Request(subscriber_id, subscription_params)

    @staticmethod
    def setup_subscription_with_params(
            subscriber_id,
            event_ids=[], 
            authors=[], 
            event_kinds=[], 
            referenced_event_ids=[], 
            referenced_event_authors=[],
            since=None,
            until=None,
            limit=10):
        
        subscription_params = {}
        if event_ids:
            subscription_params["ids"] = event_ids
        if authors:
            subscription_params["authors"] = authors
        if event_kinds:
            subscription_params["kinds"] = event_kinds
        if referenced_event_ids:
            subscription_params["#e"] = referenced_event_ids
        if referenced_event_authors:
            subscription_params["#p"] = referenced_event_authors
        if since:
            subscription_params["since"] = since
        if until:
            subscription_params["until"] = until
        if limit:
            subscription_params["limit"] = limit
        return Request(subscriber_id, subscription_params)