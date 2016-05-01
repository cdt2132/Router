#Caroline Trimble
#Router.py
#Networks, HW 6
#Main file for routing programming assignment

#------IMPORT STATEMENTS-----------#
import sys
import socket
import log
import cPickle
import send
import select
import time
import receive


#----------BEGIN CODE--------------#
#Initialization Function
def init():
    listen_port = int(sys.argv[1])
    #Gets listening port
    table = []
    peers = []
    #Sets up table and peers lists
    arg = 2
    #Adds arguments to peers and table
    while arg < len(sys.argv):
        a = sys.argv[arg]
        a = a.split(":")
        ip = a[0]
        if any(c.isalpha() for c in ip):
            try:
                ip = socket.gethostbyname(ip)
                a[0] = ip
            except:
                "Print invalid domain"
        port = int(a[1])
        hops = int(a[2])
        a.append(arg - 1)
        i = int(arg-1)
        p = [i, ip, port, hops]
        peers.append(p)
        table.append(a)
        arg += 1
    #Creates listening socket
    try:
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "Listen Socket Created"
    except socket.error:
        print "Unable to create listen socket"
    #Binds to listening Socket
    try:
        listen_socket.bind(('', listen_port))
    except socket.error:
        print "Failed to bind"

    #Creates send socket
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Calls start-up send message
    send.send(peers, table, send_sock, listen_port)

    #Returns the routing table, list of peers, listen_socket and port
    #and send socket
    return table, peers, listen_socket, listen_port, send_sock


#Main router method
def router():
    table, peers, listen_socket, port, send_sock = init()
    #Calls init
    t = time.time()
    #Gets current time
    log.print_log(port, table)
    #Prints initial routing table (this will be just neighbors)

    while(1):
        listen_socket.setblocking(0)
        ready = select.select([listen_socket],[],[], .005)
        #Sees if there is any data to be recieved, if so receive
        #If not, continue in the loop
        if ready[0]:
            data = listen_socket.recv(1024)
            #Receives data
            try:
                data = cPickle.loads(data)
                #After data is received, "unpickles" it
                #i.e turns it back into a list from a byte stream
                updated, peers, table = receive.update(data, table, peers, port)
                #calls the receive module's update function once the table is received
            except cPickle.UnpicklingError:
                continue
                #error handling
            if updated == True:
                log.print_log(port, table)
                #If the table was updated, print
        cur_t = time.time()
        #Gets current time
        if (cur_t - t) > 5:
            #If more than 5 seconds has gone by...
            t = cur_t
            #Sets the t to cur_t (so that the loop can be executed again)
            send.send(peers, table, send_sock, port)
            #Calls the send method to send its table to all its peers








router()
