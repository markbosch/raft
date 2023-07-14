import pickle

from curio import run, spawn, tcp_server

from messages import AppendEntries, AppendEntriesResult

# -- Raft Follower

async def handler(client, addr):
    print(f'connection from', addr)
    while True:
        data = await client.recv(1024)
        if not data:
            break

        message = pickle.loads(data)
        print(message)
        result = AppendEntriesResult(message.term, True)
        message = pickle.dumps(result)
        await client.sendall(message)
    await client.close()


def main(portno=6002):
    run(tcp_server, '', portno, handler)
