#Caroline Trimble
#Networks Homework 6
#Function that Updates

import socket

#Update function
def update(message, table, peers, listen_port):
    ip = message[0]
    port = message[1]
    found = False
    updated = False
    #Boolean variables
    my_ip = socket.gethostbyname(socket.gethostname())
    #Gets own IP
    for element in peers:
        if element[1] == ip and element[2] == port:
            interface = element[0]
            hops = element[3]
            found = True
        #Goes through peers to try to find which interface the
        #Message was from
    if found == False:
        #If you didn't find the message in your peers then add it
        #I am assuming that this is a symmetric, bidirectional graph
        #Thus, this just makes up for any mistakes on the commandline
        #such as forgetting to add it to the neighbors when you start up
        i = 2
        while i < len(message):
            if message[i][0] == my_ip and int(message[i][1]) == listen_port:
                #Finds self in the routing talbe it just received
                interface = len(peers)
                #Sets interface to what would be the next value in peers
                table.append([message[i][0], message[i][1], message[i][2], interface])
                #Adds to the routing table
                hops = int(message[i][2])
                ip = message[i][0]
                port = int(message[i][1])
                p = [interface, ip, port, hops]
                peers.append(p)
                #Adds to peers
                updated = True
                #Sets updated to true
            i += 1
    i = 2
    while i < len(message):
        #Goes through all the messages
        address = message[i][0]
        p = int(message[i][1])
        h = int(message[i][2])
        s = int(h + hops)
        #Gets variables
        self = False
        match = False
        if str(address) == str(my_ip) and str(p) == str(listen_port):
            self = True
            #Checks to see whether that entry in the sender's routing
            #table is just itself, if so, it just continues
        if self == False:
            #If the routing table entry is not itself
            for element in table:
                t_ip = element[0]
                t_port = element[1]
                t_hops = int(element[2])
                #Gets current table values
                if str(address) == str(t_ip) and str(p) == str(t_port):
                    #If current table values are equal to the entry in the
                    #sender table
                    match = True
                    if s < int(t_hops):
                        element[2] = s
                        element[3] = interface
                        updated = True
                        #If the distance to the next node, plus their
                        #distance to that node is lower than the
                        #distance we already have recorded, we
                        #replace that info in our routing table
            if match == False:
                table.append([address, p, s, interface])
                updated = True
                #If that entry is not found in our routing table
                #Add it 
        i+=1
    return updated, peers, table

