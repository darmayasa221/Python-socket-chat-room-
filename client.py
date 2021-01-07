import socket
import threading


username = input("Masukkan Username : ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('ip example : 127.0.0.1', 'port example : 8888'))


def receive():
    while True:
        try:
            msg = s.recv(1024).decode('ascii')
            if msg == 'USER':
                s.send(username.encode('ascii'))
            else:
                print(msg)
        except:
            print('terjadi kesalahan')
            s.close()
            break


def write():
    while True:
        msg = f'{username}: {input("Masukkan Pesan : ")}'
        s.send(msg.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
