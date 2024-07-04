import socket

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(('localhost',12345))


msg = socket.recv(1024).decode('utf-8')
print(msg)
try:
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
            socket.send(command.encode('utf-8'))
            response = (socket.recv(1024).decode('utf-8'))
            print(response)
            break

        if command == '1':
            socket.send(command.encode('utf-8'))
            response = (socket.recv(1024).decode('utf-8'))
            print(response)
        else:
            socket.send(command.encode('utf-8'))
            response = socket.recv(1024).decode('utf-8')
            print(response)
            Name = input()
            socket.send(Name.encode('utf-8'))
            msg = (socket.recv(1024).decode('utf-8'))
            print(msg)
finally:
    socket.close()







