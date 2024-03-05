import select
import socket
import threading
from collections import deque
from dataclasses import dataclass

from common import (CHUNK_SIZE, MESSAGE_END_SEQUENCE, SERVER_ADDRESS,
                    SERVER_PORT, Address, Message, MessageType, send_message)


@dataclass
class ConnectionInfo:
    messages_to_send: deque[Message]
    udp_buffer: deque[bytes]
    udp_addr: Address
    user_name: str


tcp_info_by_address: dict[Address, ConnectionInfo] = {}
udp_info_by_address: dict[Address, ConnectionInfo] = {}


def main() -> None:
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket,
    ):
        tcp_socket.bind((SERVER_ADDRESS, SERVER_PORT))
        udp_socket.bind((SERVER_ADDRESS, SERVER_PORT))

        threading.Thread(target=handle_udp_connection, args=(udp_socket,)).start()

        tcp_socket.listen()
        while True:
            tcp_conn, addr = tcp_socket.accept()
            print(f"Connected by {addr}")
            threading.Thread(
                target=handle_connection, args=(tcp_conn, udp_socket, addr)
            ).start()


def handle_connection(
    tcp_conn: socket.socket, udp_conn: socket.socket, addr: Address
) -> None:
    buffer = b""
    while True:
        if tcp_conn.fileno() == -1:
            print(f"Connection with {addr} closed")
            break

        readable, _, _ = select.select([tcp_conn], [], [], 1)
        if tcp_conn in readable:
            buffer = handle_tcp_connection(tcp_conn, addr, buffer)

        connection_info = tcp_info_by_address.get(addr)
        messages_queue = getattr(connection_info, "messages_to_send", None)
        udp_queue = getattr(connection_info, "udp_buffer", None)
        while messages_queue:
            print("sending message")
            message = messages_queue.popleft()
            send_message(tcp_conn, message)

        while udp_queue:
            print("sending udp message")
            udp_message = udp_queue.popleft()
            udp_conn.sendto(udp_message, connection_info.udp_addr)


def handle_tcp_connection(
    tcp_conn: socket.socket, addr: Address, buffer: bytes
) -> bytes:
    while MESSAGE_END_SEQUENCE not in buffer:
        buffer += tcp_conn.recv(CHUNK_SIZE)

    message = buffer[: buffer.index(MESSAGE_END_SEQUENCE)]
    buffer = buffer[buffer.index(MESSAGE_END_SEQUENCE) + len(MESSAGE_END_SEQUENCE) :]
    message = Message.deserialize(message)
    response = handle_user_message(message, addr)
    if response is not None:
        send_message(tcp_conn, response)

    return buffer


def handle_udp_connection(udp_conn: socket.socket) -> None:
    while True:
        data, addr = udp_conn.recvfrom(CHUNK_SIZE)
        print(f"Received UDP message from {addr}")
        for a, info in udp_info_by_address.items():
            if a != addr:
                info.udp_buffer.append(data)


def handle_user_message(message: Message, addr: Address) -> Message | None:
    match message.message_type:
        case MessageType.CONNECT:
            return handle_CONNECT(message, addr)
        case MessageType.MESSAGE:
            return handle_MESSAGE(message, addr)
        case MessageType.DISCONNECT:
            return handle_DISCONNECT(message, addr)
        case _:
            print("Unknown message type")


def handle_CONNECT(message: Message, addr: Address) -> Message:
    if user_with_such_name_exists(message.user_name):
        return Message(
            message_type=MessageType.ERROR,
            user_name=message.user_name,
            message="User already connected",
        )

    print(f"User {message.user_name} connected")
    udp_addr = tuple[str, int](message.udp_addr)
    tcp_info_by_address[addr] = ConnectionInfo(
        messages_to_send=deque(),
        udp_buffer=deque(),
        user_name=message.user_name,
        udp_addr=udp_addr,
    )
    udp_info_by_address[udp_addrw] = tcp_info_by_address[addr]

    return Message(message_type=MessageType.CONNECT, user_name=message.user_name)


def user_with_such_name_exists(user_name: str) -> bool:
    return any(info.user_name == user_name for info in tcp_info_by_address.values())


def handle_MESSAGE(message: Message, addr: Address) -> Message | None:
    connection_info = tcp_info_by_address[addr]
    user_name = connection_info.user_name
    if user_name != message.user_name:
        return Message(
            message_type=MessageType.ERROR,
            user_name=message.user_name,
            message="Invalid user name!",
        )

    print(f"User {user_name} sent message: {message.message}")

    queues = [
        info.messages_to_send for a, info in tcp_info_by_address.items() if addr != a
    ]

    for q in queues:
        q.append(message)


def handle_DISCONNECT(_message: Message, addr: Address) -> None:
    connection_info = tcp_info_by_address[addr]
    print(f"User {connection_info.user_name} disconnected")
    try:
        del tcp_info_by_address[addr]
        del udp_info_by_address[connection_info.udp_addr]
    except KeyError:
        print(f"User with add {addr} not found")


if __name__ == "__main__":
    main()
