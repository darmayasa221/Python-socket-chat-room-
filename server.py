import threading
import socket

host = '127.0.0.1'
port = 8888

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
            broadcast(f'-->{username} keluar dari obrolan!'.encode('ascii'))
            usernames.remove(username)
            break


def receive():
    while True:
        try:
            client, address = s.accept()
        except KeyboardInterrupt:
            print('Server dimatikan!\n')
            client.close()
            break
        print(f"terhubung dengan alamat {str(address)}")
        client.send(
            'Selamat Data Di Applikasi Chat UAS NetProg'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)
        print(f'Dari user {username}')
        print(f'{usernames} Daftar User')
        client.send('terhubung ke server \n'.encode('ascii'))
        broadcast(
            f'{username} tergabung dalam obrolan :D \n'.encode('ascii'))
        broadcast(f'Anggota chat -> {usernames}'.encode('ascii'))
        client.send('\n Masukkan Pesan: '.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    s.close()


print('server is listening...')
receive()
