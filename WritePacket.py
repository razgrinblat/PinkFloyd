import struct
from Config_reader import read_config

# Reading configuration from the 'Config.ini' file
config = read_config('Config.ini')
BUFFER_SIZE = int(config['Server']['BUFFER_SIZE'])


def write_packet(request_code: int, data: str, error_code: int) -> bytes:
    """
        This function creates a packet with a request code, data, and an error code.

        :param request_code: An integer representing the request code.
        :param data: A string containing the data to be included in the packet.
        :param error_code: An integer representing the error code.
        :return: A bytes object representing the packed data.
        """
    # Encoding the data string to bytes
    data_bytes = data.encode()
    # Trimming or padding the data to fit the buffer size
    if len(data_bytes) > BUFFER_SIZE:
        data_bytes = data_bytes[:BUFFER_SIZE]  # Trimming the data if it exceeds the buffer size
    else:
        data_bytes = data_bytes.ljust(BUFFER_SIZE, b'\x00')  # Padding the data with null bytes if it's shorter than the buffer size

    # Packing the request code, data, and error code into a bytes object
    packet = struct.pack('I1024sI', request_code, data_bytes, error_code)
    return packet
