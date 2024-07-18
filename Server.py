import socket
import threading
from Data import Album
from Config_reader import read_config
from Packet import PDU

config = read_config('Config.ini')
HOST = config['Server']['HOST']
PORT = int(config['Server']['PORT'])

DATABASE_FILE = "Pink_Floyd_DB.txt"

album = Album()
albums = Album.parse_file(album, DATABASE_FILE)


def get_albums() -> str:
    """
    Function to get all the albums of Pink Floyd
    :return:
        return a message of all albums
    """
    album_list = "\n".join(album['name'] for album in albums)
    return "the albums list:\n" + album_list


def get_albums_songs(albumName: str) -> str:
    """
    Function to get all songs in a given album.
    parameters:
        albumName (str): The name of the album to search for.
    returns:
        str: A message listing the songs in the album, or "-1" if the album is not found.
      """
    msg = "The songs in the album: \n"
    found = False
    for album in albums:
        if album['name'].lower() == albumName.lower():
            found = True
            for song in album['songs']:
                msg += f'{song['name']}\n'
    if not found:
        return "-1"
    return msg


def get_song_length(songName: str) -> str:
    """
    Function to get the length of a given song
    :param songName: the name of the song
    :return: the duration of the given song
    """
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'the Duration of {songName} is: {song['duration']}'
                found = True
    if not found:
        return "-1"
    return msg


def get_song_lyrics(songName: str) -> str:
    """
    get lyrics of a given song
    :param songName:the name of the song
    :return: the lyrics of a song
    """
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                msg = f'{song['lyrics']}'
                found = True
    if not found:
        return "-1"
    return msg


def get_song_albums(songName: str) -> str:
    """
    get the album of a given song
    :param songName: the name of a song
    """
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if songName.lower() == song['name'].lower():
                found = True
                msg = f'{album['name']}'
    if not found:
        return "-1"
    return msg


def search_song_name(word: str) -> str:
    """
    search song name by a given word or char
    :param word: word or char
    :return: return the song name
    """
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if word.lower() in song['name'].lower():
                msg += f'{song['name']}\n'
                found = True
    if not found:
        msg = "-1"
    return msg


def search_song_lyrics(word: str) -> str:
    """
    search song name by a given lyric word or char
    :param word: word or char
    :return: return the song name
    """
    msg = ""
    found = False
    for album in albums:
        for song in album['songs']:
            if word.lower() in song['lyrics'].lower():
                msg += f'{song['name']}\n'
                found = True
    if not found:
        msg = "-1"
    return msg


command_map = {
    """
    command_map for all command functions
    """
    '1': get_albums,
    '2': get_albums_songs,
    '3': get_song_length,
    '4': get_song_lyrics,
    '5': get_song_albums,
    '6': search_song_name,
    '7': search_song_lyrics,
}


def handle_client(communication_socket):
    welcome_msg = "Welcome to the Pink Floyd Server"
    communication_socket.send(welcome_msg.encode())
    while True:

        packet = communication_socket.recv(1032)
        request_code, data, error_code = PDU.read_packet(packet)
        if request_code == 8:
            break
        elif request_code == 1:
            msg = get_albums()
            pdu = PDU(0, msg, 0)
            album_packet = pdu.write_packet()
            communication_socket.send(album_packet)
        else:
            msg = command_map[str(request_code)](data)
            if msg == "-1":
                error_code = 1
            else:
                error_code = 0
            pdu = PDU(0, msg, error_code)
            packet = pdu.write_packet()
            communication_socket.send(packet)
    communication_socket.close()


def initializeServerSocket():
    """
    Connect and listen to specific port and IP
    :return: return the server socket
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
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
