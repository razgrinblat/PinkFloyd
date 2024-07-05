import socket
import threading
import Data

DATABASE_FILE = "Pink_Floyd_DB.txt"

albums = Data.parse_file(DATABASE_FILE)


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
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'the Duration of {songName} is: {song['duration']}'
                found = True
    if not found:
        return "Song not found"
    return msg


def getSongLyrics(songName):
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                found = True
                msg = f'{song['lyrics']}'
    if not found:
        return "Song not found"
    return msg


def get_song_albums(songName):
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                found = True
                msg = f'{album['name']}'
    if not found:
        return "Song not found"
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
        msg = "Song not found."
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
        msg = "Song not found."
    return msg


command_map = {
    '1': getAlbums,
    '2': (getAlbumsSongs,"Enter the album Name:"),
    '3': (getSongLength,"Enter a song Name:"),
    '4': (getSongLyrics,"Enter a song Name:"),
    '5': (get_song_albums,"Enter a song name:"),
    '6': (SearchSongName,"Enter a Word:"),
    '7': (SearchSongLyrics,"Enter a Word:"),
}


def command_helper(socket, text: str, case: str):
    socket.send(text.encode('utf-8'))
    name = socket.recv(1024).decode('utf-8')
    msg = command_map[case][0](name)
    socket.send(msg.encode('utf-8'))


def handle_client(communication_socket):
    communication_socket.send("Welcome to the Pink Floyd Server".encode())
    while True:
        command = communication_socket.recv(1024).decode()

        if command == '1':
            msg = getAlbums()
            communication_socket.send(msg.encode())
        elif command == '8':
            communication_socket.send("Bye Bye!".encode())
            break
        else:
            command_helper(communication_socket, command_map[command][1], command)
    communication_socket.close()

def initializeServerSocket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    print("Connected to Server")
    server_socket.listen(5)
    return server_socket

def multi_client(socket):
    try:
        while True:
            client_socket, client_address = socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    finally:
        socket.close()


def main():
    server_socket = initializeServerSocket()
    multi_client(server_socket)


if __name__ == "__main__":
    main()