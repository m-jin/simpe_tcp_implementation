from socket import socket, AF_INET, SOCK_DGRAM, timeout
from sys import argv
from header import ip_checksum

if __name__ == "__main__":
    dest_addr = argv[1]
    dest_port = int(argv[2])
    dest = (dest_addr, dest_port)
    window = argv[3]
    segment_size = argv[4]
    filename = argv[5]

    with open(filename, "r") as f:
        content = f.read()

    send_sock = socket(AF_INET, SOCK_DGRAM)
    rec_sock = socket(AF_INET, SOCK_DGRAM)

    rec.bind((HOST, 0))
    info = '|'.join(map(str, r.getsockname()))

    rec_sock.settimeout()

    offset = 0
    sequence = 0

    send_sock.sendto("SYN|" + info, dest)

    while offset < len(content):
        if offset + segment_size > len(content):
            segment = content[offset:]
        else:
            segment = content[offset:offset + segment_size]
        offset += segment_size

        ack_received = False
        while not ack_received:
            send_sock.sendto(ip_checksum(segment) + str(sequence) + segment, dest)

            try:
                message, address = rec_sock.recfrom(2048)
            except timeout:
                print ("Timeout")
            else:
                print (message)
                checksum = message[:2]
                ack_sequence = message[5]
                if ip_checksum(message[2:]) == checksum and ack_sequence == str(sequence):
                    ack_received = True

        sequence = 1 - sequence
