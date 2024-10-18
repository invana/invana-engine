from abc import ABC, abstractmethod
# from ..requests

class EventBase(ABC):
    
    def __init__(self):
        pass

    def request_created(self, request):
        pass

    def request_started(self, request):
        pass

    def response_received(self, request):
        pass
