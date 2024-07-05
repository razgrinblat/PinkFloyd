import socket

PORT = 12345
HOST = '127.0.0.1'


def send_and_receive(socket, message):
    socket.send(message.encode('utf-8'))
    print(socket.recv(1024).decode('utf-8'))


def initialize_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def command_handler(socket):
    while True:
        print('''
        1 Get Albums                   
        2 Get Album Songs
        3 Get Song Length
        4 Get Song Lyrics
        5 Get Song Album
        6 Search Song by Name
        7 Search Song by Lyrics
        8 Quit
        ======================
        enter a number: 
        ''')
        command = input(">>")

        if command == '8':
            send_and_receive(socket, command)
            break

        elif command == '1':
            send_and_receive(socket, command)
        else:
            send_and_receive(socket, command)
            name = input()
            send_and_receive(socket,name)

    socket.close()


def main():
    socket = initialize_socket()
    msg = socket.recv(1024).decode('utf-8')
    print(msg)
    command_handler(socket)


if __name__ == "__main__":
    main()
