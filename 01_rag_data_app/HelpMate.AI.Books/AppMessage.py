from enum import Enum

class MessageType(Enum):
    Simple = 1
    Info = 2
    Warnings = 3
    Error=4
    Success=5


class AppMessage:
    def __init__(self):
        self.Request=None
        self.Response_Message=None
        self.Success=False
        self.Data=None
        self.Message_Type:MessageType=MessageType.Simple
