import threading
import socket

host = 'ip example : 127.0.0.1'
port = 'port example : 8888'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(100)

clients = []
usernames = []


def broadcast(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} keluar dari obrolan!'.encode('ascii'))
            usernames.remove(username)
            break


def receive():
    while True:
        client, address = s.accept()
        print(f"terhubung dengan {str(address)}")

        client.send('USER'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(f'Dari user {username}')
        broadcast(f'{username} tergabung dalam obrolan'.encode('ascii'))
        client.send('terhubung ke server '.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start


print('server is listening...')

receive()
