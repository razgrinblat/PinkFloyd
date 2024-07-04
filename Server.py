import socket
import threading
import Data

albums = Data.parse_file("Pink_Floyd_DB.txt")


def getAlbums():
    album_list = "\n".join(album['name'] for album in albums)
    return "the albums list:\n" + album_list


def getAlbumsSongs(albumName):
    msg = "The songs in the album: \n"
    for album in albums:
        if album['name'].lower() == albumName.lower():
            for song in album['songs']:
                msg += f'{song['name']}\n'
    return msg


def getSongLength(songName):
    msg = ""
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'the Duration of {songName} is: {song['duration']}'
    return msg


def getSongLyrics(songName):
    msg = ""
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'{song['lyrics']}'
    return msg


def getSongAlbums(songName):
    msg = ""
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'{album['name']}'
                return msg


def SearchSongName(word):
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if word.lower() in song['name'].lower():
                msg += f'{song['name']}\n'
                found = True
    if not found:
        msg = "No songs found."
    return msg


def SearchSongLyrics(word):
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if word.lower() in song['lyrics'].lower():
                msg += f'{song['name']}\n'
                found = True
    if not found:
        msg = "No songs found."
    return msg


def handle_client(communication_socket):
    communication_socket.send("Welcome to the Pink Floyd Server".encode('utf-8'))
    while True:
        command = communication_socket.recv(1024).decode('utf-8')

        match command:
            case '1':
                msg = getAlbums()
                communication_socket.send(msg.encode('utf-8'))
            case '2':
                communication_socket.send("Enter the album Name:".encode('utf-8'))
                albumName = communication_socket.recv(1024).decode('utf-8')
                msg = getAlbumsSongs(albumName)
                communication_socket.send(msg.encode('utf-8'))
            case '3':
                communication_socket.send("Enter a song Name:".encode('utf-8'))
                songName = communication_socket.recv(1024).decode('utf-8')
                msg = getSongLength(songName)
                communication_socket.send(msg.encode('utf-8'))

            case '4':
                communication_socket.send("Enter a song Name:".encode('utf-8'))
                songName = communication_socket.recv(1024).decode('utf-8')
                msg = getSongLyrics(songName)
                communication_socket.send(msg.encode('utf-8'))

            case '5':
                communication_socket.send("Enter a song name:".encode('utf-8'))
                songName = communication_socket.recv(1024).decode('utf-8')
                msg = getSongAlbums(songName)
                communication_socket.send(msg.encode('utf-8'))

            case '6':
                communication_socket.send("Enter a Word:".encode('utf-8'))
                word = communication_socket.recv(1024).decode('utf-8')
                msg = SearchSongName(word)
                communication_socket.send(msg.encode('utf-8'))
            case '7':
                communication_socket.send("Enter a Word:".encode('utf-8'))
                word = communication_socket.recv(1024).decode('utf-8')
                msg = SearchSongLyrics(word)
                communication_socket.send(msg.encode('utf-8'))
            case '8':
                communication_socket.send("Bye Bye!".encode('utf-8'))
                break

    communication_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
print("Connected to Server")
server_socket.listen(5)

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
finally:
    server_socket.close()
