import json
import socket
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

type Address = tuple[str, int]

SERVER_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 8765
CHUNK_SIZE: int = 1024
ENCODING = "utf-8"

MESSAGE_END_SEQUENCE = b"\r\n\r\n"


class MessageType(StrEnum):
    CONNECT = "CONNECT"
    MESSAGE = "MESSAGE"
    DISCONNECT = "DISCONNECT"
    ERROR = "ERROR"


class Serializable:
    def serialize(self) -> bytes:
        return json.dumps(self.__dict__).encode(encoding=ENCODING)

    @classmethod
    def deserialize(cls, serialized: bytes) -> Self:
        decoded = serialized.decode(encoding=ENCODING)
        try:
            return cls(**json.loads(decoded))  # type: ignore
        except Exception as e:
            print(f"Error deserializing {decoded}")
            raise e


@dataclass
class Message(Serializable):
    message_type: MessageType
    user_name: str | None = None
    message: str | None = None
    udp_addr: Address | None = None

    def __str__(self) -> str:
        return f"Message({self.message_type}, {self.user_name})"


def send_message(conn: socket.socket, message: Message) -> None:
    return conn.sendall(message.serialize() + MESSAGE_END_SEQUENCE)
