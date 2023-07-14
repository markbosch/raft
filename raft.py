# raft.py

import pickle

from curio import TaskGroup, Kernel, sleep
from curio.socket import socket, AF_INET, SOCK_STREAM
from curio.debug import *
from curio.monitor import Monitor

from messages import AppendEntries, AppendEntriesResult


# --- Raft Leader
peers = []

kernel = Kernel(debug=[longblock, logcrash])

async def leader_election_loop():
    ...

async def message_loop():
    ...

async def heartbeat_loop():
    print("heartbeat")
    while True:
        await sleep(5)
        for address in peers:
            await _send_append_entries(address, 1, 6001, 2, 3, [], 4)

async def _send_append_entries(
        peer_address, term, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
    # send over socket
    try:
        async with socket(AF_INET, SOCK_STREAM) as sock:
            await sock.connect(peer_address)
            
            append_entries = AppendEntries(
                term, leader_id, prev_log_index, prev_log_term, entries, leader_commit)
            message = pickle.dumps(append_entries)

            await sock.sendall(message)

            response = await sock.recv(1024)
            response = pickle.loads(response)
            print(f'Got response: {response}')
            
    except Exception as e:
        print(f"Error sending AppendEntries to {peer_id}: {str(e)}")

def add_peers():
    peers.append(('localhost', 6002))
    peers.append(('localhost', 6003))

def add_peer(address):
    peers.append(address)

async def start():
    print('start')
    async with TaskGroup() as group:
        await group.spawn(leader_election_loop)
        await group.spawn(message_loop)
        await group.spawn(heartbeat_loop)

def main(defaults=False):
    if defaults:
        add_peers()

    kernel.run(start(), shutdown=True)
