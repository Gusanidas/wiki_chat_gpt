from typing import List, NewType, TypedDict

class Message(TypedDict):
    content: str
    role: str

ConversationLogType = List[Message]
ConversationLog = NewType('ConversationLog', ConversationLogType)
