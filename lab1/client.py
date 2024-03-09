import select
import socket
import sys
from uuid import uuid4

from common import (CHUNK_SIZE, MESSAGE_END_SEQUENCE, SERVER_ADDRESS,
                    SERVER_PORT, Message, MessageType, send_message)

buffer: bytes = b""
EXIT_MESSAGE: str = "exit"
UDP_TRANSMISSION_MESSAGE: str = "U"
UDP_DATA = '''
                                 _______
                           _,,ad8888888888bba,_
                        ,ad88888I888888888888888ba,
                      ,88888888I88888888888888888888a,
                    ,d888888888I8888888888888888888888b,
                   d88888PP"""" ""YY88888888888888888888b,
                 ,d88"'__,,--------,,,,.;ZZZY8888888888888,
                ,8IIl'"                ;;l"ZZZIII8888888888,
               ,I88l;'                  ;lZZZZZ888III8888888,
             ,II88Zl;.                  ;llZZZZZ888888I888888,
            ,II888Zl;.                .;;;;;lllZZZ888888I8888b
           ,II8888Z;;                 `;;;;;''llZZ8888888I8888,
           II88888Z;'                        .;lZZZ8888888I888b
           II88888Z; _,aaa,      .,aaaaa,__.l;llZZZ88888888I888
           II88888IZZZZZZZZZ,  .ZZZZZZZZZZZZZZ;llZZ88888888I888,
           II88888IZZ<'(@@>Z|  |ZZZ<'(@@>ZZZZ;;llZZ888888888I88I
          ,II88888;   `""" ;|  |ZZ; `"""     ;;llZ8888888888I888
          II888888l            `;;          .;llZZ8888888888I888,
         ,II888888Z;           ;;;        .;;llZZZ8888888888I888I
         III888888Zl;    ..,   `;;       ,;;lllZZZ88888888888I888
         II88888888Z;;...;(_    _)      ,;;;llZZZZ88888888888I888,
         II88888888Zl;;;;;' `--'Z;.   .,;;;;llZZZZ88888888888I888b
         ]I888888888Z;;;;'   ";llllll;..;;;lllZZZZ88888888888I8888,
         II888888888Zl.;;"Y88bd888P";;,..;lllZZZZZ88888888888I8888I
         II8888888888Zl;.; `"PPP";;;,..;lllZZZZZZZ88888888888I88888
         II888888888888Zl;;. `;;;l;;;;lllZZZZZZZZW88888888888I88888
         `II8888888888888Zl;.    ,;;lllZZZZZZZZWMZ88888888888I88888
          II8888888888888888ZbaalllZZZZZZZZZWWMZZZ8888888888I888888,
          `II88888888888888888b"WWZZZZZWWWMMZZZZZZI888888888I888888b
           `II88888888888888888;ZZMMMMMMZZZZZZZZllI888888888I8888888
            `II8888888888888888 `;lZZZZZZZZZZZlllll888888888I8888888,
             II8888888888888888, `;lllZZZZllllll;;.Y88888888I8888888b,
            ,II8888888888888888b   .;;lllllll;;;.;..88888888I88888888b,
            II888888888888888PZI;.  .`;;;.;;;..; ...88888888I8888888888,
            II888888888888PZ;;';;.   ;. .;.  .;. .. Y8888888I88888888888b,
           ,II888888888PZ;;'                        `8888888I8888888888888b,
           II888888888'                              888888I8888888888888888b
          ,II888888888                              ,888888I88888888888888888
         ,d88888888888                              d888888I8888888888ZZZZZZZ
      ,ad888888888888I                              8888888I8888ZZZZZZZZZZZZZ
    ,d888888888888888'                              888888IZZZZZZZZZZZZZZZZZZ
  ,d888888888888P'8P'                               Y888ZZZZZZZZZZZZZZZZZZZZZ
 ,8888888888888,  "                                 ,ZZZZZZZZZZZZZZZZZZZZZZZZ
d888888888888888,                                ,ZZZZZZZZZZZZZZZZZZZZZZZZZZZ
888888888888888888a,      _                    ,ZZZZZZZZZZZZZZZZZZZZ888888888
888888888888888888888ba,_d'                  ,ZZZZZZZZZZZZZZZZZ88888888888888
8888888888888888888888888888bbbaaa,,,______,ZZZZZZZZZZZZZZZ888888888888888888
88888888888888888888888888888888888888888ZZZZZZZZZZZZZZZ888888888888888888888
8888888888888888888888888888888888888888ZZZZZZZZZZZZZZ88888888888888888888888
888888888888888888888888888888888888888ZZZZZZZZZZZZZZ888888888888888888888888
8888888888888888888888888888888888888ZZZZZZZZZZZZZZ88888888888888888888888888
88888888888888888888888888888888888ZZZZZZZZZZZZZZ8888888888888888888888888888
8888888888888888888888888888888888ZZZZZZZZZZZZZZ88888888888888888888888888888
88888888888888888888888888888888ZZZZZZZZZZZZZZ8888888888888888888888888888888
8888888888888888888888888888888ZZZZZZZZZZZZZZ88888888888888888888888888888888
'''


def main() -> None:
    user_name = input("Enter your user name: ") or str(uuid4())
    with (
        socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket,
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket,
    ):
        tcp_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        udp_socket.connect((SERVER_ADDRESS, SERVER_PORT))
        connect_with_server(tcp_socket, udp_socket, user_name)

        while True:
            read, _, _ = select.select([tcp_socket, udp_socket, sys.stdin], [], [])

            if tcp_socket in read:
                handle_tcp_received_messages(tcp_socket)
            if udp_socket in read:
                handle_udp_received_messages(udp_socket)
            if sys.stdin in read:
                handle_user_input(tcp_socket, udp_socket, user_name)


def connect_with_server(
    tcp_socket: socket.socket, udp_socket: socket.socket, user_name: str
) -> None:
    global buffer
    print("Connected to server")
    message = Message(
        message_type=MessageType.CONNECT,
        user_name=user_name,
        udp_addr=udp_socket.getsockname(),
    )

    send_message(tcp_socket, message)
    buffer += tcp_socket.recv(CHUNK_SIZE)
    message = buffer[: buffer.index(MESSAGE_END_SEQUENCE)]
    buffer = buffer[buffer.index(MESSAGE_END_SEQUENCE) + len(MESSAGE_END_SEQUENCE) :]
    decoded_message = Message.deserialize(message)
    if decoded_message.message_type == MessageType.ERROR:
        print("Username already taken")
        exit(1)


def disconnect_from_server(conn: socket.socket) -> None:
    print("Disconnected from server")
    message = Message(message_type=MessageType.DISCONNECT)

    send_message(conn, message)
    exit(0)


def handle_user_input(
    tcp_conn: socket.socket, udp_conn: socket.socket, user_name: str
) -> None:
    message = sys.stdin.readline().strip()
    if message == EXIT_MESSAGE:
        disconnect_from_server(tcp_conn)
        return
    elif message == UDP_TRANSMISSION_MESSAGE:
        send_udp_message(udp_conn, UDP_DATA)
        return

    send_message(
        tcp_conn,
        Message(message_type=MessageType.MESSAGE, user_name=user_name, message=message),
    )


def send_udp_message(conn: socket.socket, message: str) -> None:
    encoded = message.encode()
    while encoded:
        chunk = encoded[:CHUNK_SIZE]
        encoded = encoded[CHUNK_SIZE:]
        conn.send(chunk)


def handle_tcp_received_messages(conn: socket.socket) -> None:
    global buffer
    while MESSAGE_END_SEQUENCE not in buffer:
        buffer += conn.recv(CHUNK_SIZE)

    while MESSAGE_END_SEQUENCE in buffer:
        message = buffer[: buffer.index(MESSAGE_END_SEQUENCE)]
        buffer = buffer[
            buffer.index(MESSAGE_END_SEQUENCE) + len(MESSAGE_END_SEQUENCE) :
        ]
        decoded_message = Message.deserialize(message)
        if decoded_message.message_type == MessageType.MESSAGE:
            print(f"{decoded_message.user_name}: {decoded_message.message}")
        elif decoded_message.message_type == MessageType.ERROR:
            print(f"Error: {decoded_message.message}")
            disconnect_from_server(conn)


def handle_udp_received_messages(conn: socket.socket) -> None:
    message = conn.recv(CHUNK_SIZE * 2)
    decoded = message.decode()
    print(decoded)


if __name__ == "__main__":
    main()
