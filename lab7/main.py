import subprocess
from functools import partial
from typing import Callable

from kazoo.client import KazooClient
import argparse

from kazoo.exceptions import NoNodeException
from kazoo.protocol.states import ZnodeStat, WatchedEvent

parser = argparse.ArgumentParser(description='Zookeeper client')
parser.add_argument("--port", type=int, default=2181, help="Zookeeper port")
parser.add_argument("--exec", type=str, default="python3 simplest_gui.py",
                    help="Command to execute when the node is created")
args = parser.parse_args()

HOST = f"127.0.0.1:{args.port}"
WATCHED_NODE_NAME = "/a"

zk = KazooClient(hosts=HOST)
process = None

watched_children = set()


def ignore_first_call(func: Callable) -> Callable:
    already_called = False

    def wrapper(*args, **kwargs):
        nonlocal already_called
        if not already_called:
            already_called = True
            return
        return func(*args, **kwargs)

    return wrapper


@zk.DataWatch(WATCHED_NODE_NAME)
def watch_node(_data: bytes | None, _stat: ZnodeStat | None, event: WatchedEvent | None) -> None:
    if event is None:
        return

    global process
    if event.type == "CREATED":
        process = subprocess.Popen(args.exec.split(" "))
        print(f"Node {WATCHED_NODE_NAME} created")
        zk.ChildrenWatch(WATCHED_NODE_NAME)(partial(ignore_first_call(watch_children), path=WATCHED_NODE_NAME))

    elif event.type == "DELETED":
        if process is not None:
            process.kill()
        print(f"Node {WATCHED_NODE_NAME} deleted")


def watch_children(children_: list[str], path: str) -> None:
    for child in children_:
        child_path = f"{path}/{child}"
        if child_path not in watched_children:
            zk.ChildrenWatch(child_path)(partial(ignore_first_call(watch_children), path=child_path))
            watched_children.add(child_path)

    print(f"Total nodes count: {len(get_nodes_names(WATCHED_NODE_NAME))}")


def print_tree(node: str, level: int = 0) -> None:
    try:
        children = zk.get_children(node)
    except NoNodeException:
        return
    local_node_name = "/" + node.strip("/").split("/")[-1]
    print("  " * level + local_node_name)
    for child in children:
        print_tree(f"{node}/{child}", level + 1)


def get_nodes_names(node: str) -> list[str]:
    try:
        children = zk.get_children(node)
    except NoNodeException:
        return []
    nodes = [node]
    for child in children:
        nodes += get_nodes_names(f"{node}/{child}")

    if node == WATCHED_NODE_NAME:
        watched_children.clear()
        watched_children.update(nodes)

    return nodes


zk.start()

try:
    while True:
        command = input(">>> ")

        if command == "exit":
            break
        elif command == "tree":
            print_tree(WATCHED_NODE_NAME)
finally:
    zk.stop()
    zk.close()
