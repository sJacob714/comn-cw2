from cmath import inf
from socket import *
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")

EOF = 0
sequenceNum = -1
print("The receiver is ready to recieve")
# loops until end of file is received
while EOF==0:
    
    message, senderAddress = receiverSocket.recvfrom(1027)
    receiverSocket.sendto(message[0:2], senderAddress)

    # Checks if previously acknowledged packet was resent
    if (sequenceNum == int.from_bytes(message[0:2], 'little')):
        continue
    
    # writes to file
    sequenceNum = int.from_bytes(message[0:2], 'little')
    EOF = message[2]
    data = message[3:]
    file.write(data)

#To make sure final ACK is recieved by sender
for i in range(20):
    receiverSocket.sendto(message[0:2], senderAddress)

receiverSocket.close()
file.close()