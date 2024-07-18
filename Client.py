import socket
from Config_reader import read_config
from Packet import PDU

config = read_config('Config.ini')
HOST = config['Server']['HOST']
PORT = int(config['Server']['PORT'])
BUFFER_SIZE = int(config['Server']['BUFFER_SIZE'])


def send_and_recieve_packet(socket: socket, command: str, name: str) -> None:
    """
    function that write a packet, send it to a given socket. recieve a packet from sever, encode and print the data
    :param socket: a given socket
    :param command: command between 1 to 8
    :param name: the message to send through the socket
    :return: print the data
    """
    pdu = PDU(int(command), name, 0)
    packet = pdu.write_packet()
    socket.send(packet)
    response_packet = socket.recv(BUFFER_SIZE)
    request_code, data, error_code = PDU.read_packet(response_packet)
    if error_code == 1:
        print("invalid input")
    else:
        print(data)


def initialize_socket():
    """
    connect the socket to host and IP
    :return: return the socket
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def command_handler(socket):
    while True:
        print('''
        =====================
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
        prompt = ">>"
        command = input(prompt)

        if not command.isdigit() or int(command) <= 0 or int(command) > 8:
            print('invalid command')
            continue
        elif command == '1':
            send_and_recieve_packet(socket, command, "")
        elif command == '2':
            name = input("Enter the album Name:")
            send_and_recieve_packet(socket, command, name)
        elif command in ['3', '4', '5']:
            name = input("Enter the song Name:")
            send_and_recieve_packet(socket, command, name)
        elif command in ['6', '7']:
            name = input("enter a Word:")
            send_and_recieve_packet(socket, command, name)
        elif command == '8':
            pdu = PDU(int(command), "", 0)
            packet = pdu.write_packet()
            socket.send(packet)
            print("bye bye!")
            break

    socket.close()


def main():
    socket = initialize_socket()
    msg = socket.recv(BUFFER_SIZE).decode()
    print(msg)
    command_handler(socket)


if __name__ == "__main__":
    main()
