from cmath import inf
from socket import *
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")

maxNumOfPackets = inf       # number of packets to be received, initialised as inf until end of file packet is received
messageList = []
print("The receiver is ready to recieve")

# due to packet delay, packets could be received in wrong order
# loops until all packets are received
while (len(messageList) != maxNumOfPackets):
    message, senderAddress = receiverSocket.recvfrom(1027)

    sequenceNum = int.from_bytes(message[0:2], 'little')
    EOF = message[2]
    data = message[3:]

    #stores data and sequence number so list can be sorted at end
    messageList.append([sequenceNum, data])

    # sequence number of end of file packet will tell us the size of the packets
    if (EOF == 255):
        maxNumOfPackets = sequenceNum+1

# orders list based on sequence number, then writes all data to file
fileBytes = [item[1] for item in sorted(messageList, key = lambda x: x[0])]
for byte in fileBytes:
    file.write(byte)

receiverSocket.close()
file.close()