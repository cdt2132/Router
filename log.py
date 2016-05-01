#Caroline Trimble
#Networks, HW 6
#Function to print the log to the console

import socket
import datetime

def print_log(port, table):
    my_ip = socket.gethostbyname(socket.gethostname())
    time_stamp = str(datetime.datetime.now().time())
    print "Node %s:%d @ %s"%(my_ip, port, time_stamp)
    #Adds time stamp and own IP and port
    print "host           port   distance     interface"
    for element in table:
        print "%s    %s    %s           %s" %(element[0], element[1], element[2], element[3])
    #goes through table and prints