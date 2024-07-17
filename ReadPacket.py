import struct


def read_packet(packet: bytes):
    # Define the format string for struct.unpack, the format is Integer,String(1024 Btyes) and Integer
    format_string = 'I1024sI'

    # Unpack the packet
    request_code, data_bytes, error_code = struct.unpack(format_string, packet)

    # Decode the data bytes, removing any padding null bytes
    data = data_bytes.rstrip(b'\x00').decode()

    return request_code, data, error_code
