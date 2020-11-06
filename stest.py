from socket import socket, AF_INET, SOCK_DGRAM, timeout
from sys import argv, exit
from header import ip_checksum

if __name__ == "__main__":
    dest_addr = argv[1]
    dest_port = int(argv[2])
    dest = (dest_addr, dest_port)
    window = int(argv[3])
    segment_size = int(argv[4])
    filename = argv[5]
    HOST = 'localhost'

    with open(filename, "r") as f:
        content = f.read()

    send_sock = socket(AF_INET, SOCK_DGRAM)
    rec_sock = socket(AF_INET, SOCK_DGRAM)

    header = "SYN"
    rec_sock.bind((HOST, 0))
    addr = '|'.join(map(str, rec_sock.getsockname()))
    connection_request = header + '|' + addr + '|' + str(window)

    rec_sock.settimeout(5)

    no_of_segments = window/segment_size
    offset = 0
    sequence = 0
    attempt = 0


#START CONNECTION with 3-WAY HANDSHAKE

    while attempt < 3:
        try:
            send_sock.sendto(connection_request, dest)
            print "establishing connection..."
            message, address = rec_sock.recvfrom(50)
            print message
            if message == "SYN-ACK":
                header = "ACK"
                send_sock.sendto(header, dest)
                break
        except timeout:
            print "Timeout"
            attempt += 1
            if attempt == 3:
                print "connection failed"
                exit()


#SEND PACKETS

    while offset < len(content):
        print "test"
        if offset + segment_size > len(content):
            segment = content[offset:]
        else:
            segment = content[offset:offset + segment_size]
        offset += segment_size

        ack_received = False
        while not ack_received:
            # while sequence < sequence + no_of_segments:
            print sequence
            send_sock.sendto(ip_checksum(segment) + str(sequence) + segment, dest)
            # sequence += 1
            try:
                message, address = rec_sock.recvfrom(50)
            except timeout:
                print ("Timeout")
                exit()
            else:
                print (message)
                checksum = message[:2]
                ack_sequence = message[5]
                if ip_checksum(message[2:]) == checksum and ack_sequence == str(sequence):
                    ack_received = True
        sequence += 1
        


#TEAR DOWN - 3 SEGMENT

    header = 'FIN'
    attempt = 0

    while attempt < 3:
        try:
            send_sock.sendto(header, dest)
            end = rec_sock.recv(10)
            if end == 'ACK':
                send_sock.sendto(header, dest)
                print 'connection ended.'
                exit()
        except timeout:
            print "Attempting to end connection"
            attempt += 1

    print "Receiver connection not terminated."
    exit()





