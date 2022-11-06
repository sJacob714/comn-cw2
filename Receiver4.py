from cmath import inf
from socket import *
import time
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])
windowSize = int(sys.argv[3])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")


buffer = [None]*windowSize  # list of buffered packets, waiting for missing packets to be received
EOF = 0                     # Used to see if end of file packet has been received yet
bufferBias = 0              # Sequence number of first item in buffer

startTime = time.time()
acksReceived = 0

print("The receiver is ready to recieve")
# loops until End of file packet is found and buffer is empty
while (EOF==0) or not (all(item is None for item in buffer)):
    message, senderAddress = receiverSocket.recvfrom(1027)
    acksReceived+=1

    # if packet was previously acknowledged, Resends Ack packet
    if (int.from_bytes(message[0:2],'little')<bufferBias) or (message in buffer):
        receiverSocket.sendto(message[0:2], senderAddress)

    # When receiving packet within window, send ACK and place packet in buffer
    elif ((int.from_bytes(message[0:2],'little') - bufferBias)<windowSize):
        receiverSocket.sendto(message[0:2], senderAddress)
        # packet is placed in relation to first item in buffer (so buffer is in order)
        buffer[int.from_bytes(message[0:2],'little') - bufferBias] = message
    
    # Write all consecutive data in the buffer to the file
    while (buffer[0]!=None):
        bufferBias+=1
        EOF += buffer[0][2]
        data = buffer[0][3:]
        file.write(data)

        #remove head of buffer as data has been written to file, append None at end of buffer
        lastPacket = buffer.pop(0)
        buffer.append(None)    

# calculates average time between acks
duration = time.time()-startTime
averageTimeForAck = duration/acksReceived

# Sockets stays open for a bit longer, acking any packets received
# timer based on average time between acks, with lots of room for delay variation
receiverSocket.settimeout(averageTimeForAck*3)
keepListening = True
while keepListening:
    try:
        message, senderAddress = receiverSocket.recvfrom(1027)
        receiverSocket.sendto(message[0:2], senderAddress)
    except:
        keepListening = False

receiverSocket.close()
file.close()