import struct
from Config_reader import read_config

# Reading configuration from the 'Config.ini' file
config = read_config('Config.ini')
DATA_SIZE = 1024
# Define the format string for struct.unpack, the format is Integer,String(1024 Btyes) and Integer
FRAME_FORMAT = 'I1024sI'


class PDU:
    def __init__(self, request_code: int, data: str, error_code: int):
        self.request_code = request_code
        self.data = data
        self.error_code = error_code

    def write_packet(self) -> bytes:
        """
            This function creates a packet with a request code, data, and an error code.
            :return: A bytes object representing the packed data.
            """
        # Encoding the data string to bytes
        data_bytes = self.data.encode()
        # Trimming or padding the data to fit the buffer size
        if len(data_bytes) > DATA_SIZE:
            data_bytes = data_bytes[:DATA_SIZE]  # Trimming the data if it exceeds the buffer size
        else:
            # Padding the data with null bytes if it's shorter than the buffer size
            data_bytes = data_bytes.ljust(DATA_SIZE,b'\x00')

        # Packing the request code, data, and error code into a bytes object
        packet = struct.pack(FRAME_FORMAT, self.request_code, data_bytes, self.error_code)
        return packet

    @staticmethod
    def read_packet(packet: bytes):

        # Unpack the packet
        request_code, data_bytes, error_code = struct.unpack(FRAME_FORMAT, packet)

        # Decode the data bytes, removing any padding null bytes
        data = data_bytes.rstrip(b'\x00').decode()

        return request_code, data, error_code
