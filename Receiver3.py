from socket import *
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")

EOF = 0
prevSequenceNum = -1
expectedSequenceNum = 0
expectedSequenceNum = expectedSequenceNum.to_bytes(2, 'little')

print("The receiver is ready to recieve")
while EOF==0:
    message, senderAddress = receiverSocket.recvfrom(1027)
    while (message[0:2]!=expectedSequenceNum):
        if prevSequenceNum!=-1:
            #print("recieved ",message[0:3]," expecting ", expectedSequenceNum,"reacknowldged ", prevSequenceNum)
            receiverSocket.sendto(prevSequenceNum, senderAddress)
        message, senderAddress = receiverSocket.recvfrom(1027)
    #print("GOT CORRECT PACKET, SENT ACK ", message[0:3])
    expectedSequenceNum = (int.from_bytes(message[0:2], 'little') + 1).to_bytes(2, 'little')
    receiverSocket.sendto(message[0:2], senderAddress)
    
    EOF = message[2]
    data = message[3:]
    file.write(data)
    prevSequenceNum = message[0:2]

#To make sure final ACK is recieved by sender
for i in range(20):
    receiverSocket.sendto(message[0:2], senderAddress)

receiverSocket.close()
file.close()