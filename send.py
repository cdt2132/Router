#Caroline Trimble
#Networks, HW6
#Function to send table update to all neighbors

import socket
import cPickle

def send(peers, table, send_sock, listen_port):
    i = 0
    while i < len(peers):
        #Go through all of your "neighbors" in the peers list
        ip = peers[i][1]
        port = int(peers[i][2])
        address = (ip, port)
        #Gets IP and port
        try:
            send_sock.connect(address)
        except:
            i += 1
            continue
        #Connects to the address
        #If it tries to connect and fails, the loop just continues
        #This is so that you can start the socket before neighbors
        #are running
        my_ip = socket.gethostbyname(socket.gethostname())
        l = [my_ip, listen_port]
        t = l + table
        #Attach my own IP and listening port to the routing table
        #Thus the packet format will be "SenderIP, SenderPort, Table(list format)"
        p = cPickle.dumps(t)
        #Use C pickle to turn this "packet" into a byte stream that can be
        #Sent over sockets
        try:
            send_sock.send(p)
            #Sends the "packet"
        except:
            i += 1
            continue
            #Error handling
        i += 1


