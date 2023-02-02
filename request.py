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
        # Get a comma separated id of the authors to subscribe to
        authors_input = interface.get_input("Enter a comma-separated list of authors' pulic keys:\n>")
        if authors_input:
            array = authors_input.split(",")
            subscription_params["authors"] = [author.strip() for author in array if author.strip()]
        # Get a comma separated list of event ids to subscribe to
        event_ids_input = interface.get_input("Enter a comma-separated list of event ids:\n>")
        if event_ids_input:
            array = event_ids_input.split(",")
            subscription_params["ids"] = [event_id.strip() for event_id in array if event_id.strip()]
        # Get a comma separated list of event kinds to subscribe to
        event_kinds_input = interface.get_input("Enter a comma-separated list of event kinds:\n>")
        if event_kinds_input:
            array = event_kinds_input.split(",")
            subscription_params["kinds"] = [event_kind.strip() for event_kind in array if event_kind.strip()]
        # Get a comma separated list event ids referenced by the events to fetch
        referenced_event_ids_input = interface.get_input("Enter a comma-separated list of event ids referenced by the events to fetch:\n>")
        if referenced_event_ids_input:
            array = referenced_event_ids_input.split(",")
            subscription_params["#e"] = [event_id.strip() for event_id in array if event_id.strip()]
        # Get a comma separated list of authors referenced by the events to fetch
        referenced_event_authors_input = interface.get_input("Enter a comma-separated list of authors referenced by the events to fetch:\n>")
        if referenced_event_authors_input:
            array = referenced_event_authors_input.split(",")
            subscription_params["#p"] = [author.strip() for author in array if author.strip()]
        # Get the oldest timestamp of the events to fetch
        since_input = interface.get_input("Enter the oldest timestamp of the events to fetch:\n>")
        if since_input:
            subscription_params["since"] = since_input
        # Get the newest timestamp of the events to fetch
        until_input = interface.get_input("Enter the newest timestamp of the events to fetch:\n>")
        if until_input:
            subscription_params["until"] = until_input
        # Get the maximum number of events to fetch
        limit_input = interface.get_input("Enter the maximum number of events to fetch:\n>")
        if limit_input:
            subscription_params["limit"] = limit_input
        
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