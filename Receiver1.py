from cmath import inf
from socket import *
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")

maxNumOfPackets = inf
messageList = []
print("The receiver is ready to recieve")

while (len(messageList) != maxNumOfPackets):
    message, senderAddress = receiverSocket.recvfrom(1027)

    sequenceNum = int.from_bytes(message[0:2], 'little')
    EOF = message[2]
    data = message[3:]
    messageList.append([sequenceNum, data])

    if (EOF == 255):
        maxNumOfPackets = sequenceNum+1

fileBytes = [item[1] for item in sorted(messageList, key = lambda x: x[0])]

for byte in fileBytes:
    file.write(byte)


receiverSocket.close()
file.close()