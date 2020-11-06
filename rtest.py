from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv, stdout
from header import ip_checksum


def send(content, to):
    checksum = ip_checksum(content)
    send_sock.sendto(checksum + content, to)

expecting_seq = 0

if __name__ == "__main__":
    # dest_addr = argv[1]
    # dest_port = int(argv[2])
    # dest = (dest_addr, dest_port)
    listen_addr = "localhost"
    listen_port = int(argv[1])
    filename = argv[2]
    listen = (listen_addr, listen_port)

    send_sock = socket(AF_INET, SOCK_DGRAM)
    rec_sock = socket(AF_INET, SOCK_DGRAM)

    rec_sock.bind(listen)

    expecting_seq = 0

    a = rec_sock.recv(50)
    header = a.split("|")
    dest = (header[1], int(header[2]))
    window = int(header[3])
    print dest
    if header[0] == "SYN":
        send_sock.sendto("SYN-ACK", dest)
    elif header[0] == "ACK":
        open(filename, 'w')
    # print "Listening..."
    # message, address = rec_sock.recvfrom(100)    
    # print message, address
    # dest = ('localhost', int(address[1]))
    # print dest    
    # if message == "SYN":
    #     # rec_sock.bind(('', 0))
    #     send_sock.sendto("SYN-ACK", dest)
    # elif message == "ACK":
    #     open(filename, 'w')

    while True:
        f = open(filename, 'a')
        message, address = rec_sock.recvfrom(window)
        if message == 'FIN':
            send_sock.sendto('ACK', dest)
            message, address = rec_sock.recvfrom(window)
            if message == 'FIN':
                print'Transfer ended.'
                exit()
        else:   
            checksum = message[:2]
            seq = message[2]
            print seq
            content = message[3:]

            if ip_checksum(content) == checksum:
                send("ACK" + seq, dest)
                if seq == str(expecting_seq):
                    f.write(content)
                    stdout.write(content)
                    print seq
                    print '#####'
                    expecting_seq += 1 #- expecting_seq

            else:
                print seq
                expecting_seq += 1
                print expecting_seq
                negative_seq = str(expecting_seq)
                send("ACK" + negative_seq, dest)
