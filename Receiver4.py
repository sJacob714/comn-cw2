from socket import *
import sys

receiverPort = int(sys.argv[1])
fileName = str(sys.argv[2])
windowSize = int(sys.argv[3])

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
file = open(fileName, "wb")

buffer = [None]*windowSize
EOF = 0
prevSequenceNum = -1
bufferBias = 0
#bufferBias = bufferBias.to_bytes(2, 'little')

print("The receiver is ready to recieve")
while (EOF==0) or not (all(item is None for item in buffer)):
    message, senderAddress = receiverSocket.recvfrom(1027)
    #while (message[0:2]!=bufferBias):
    while (int.from_bytes(message[0:2],'little')<bufferBias):
    #if (int.from_bytes(message[0:2],'little')<bufferBias):
        receiverSocket.sendto(message[0:2], senderAddress)
        print("recieved ",message[0:3]," expecting ", bufferBias.to_bytes(2,'little'))
        message, senderAddress = receiverSocket.recvfrom(1027)
    #print("GOT CORRECT PACKET, SENT ACK ", message[0:3])
    #bufferBias = (int.from_bytes(message[0:2], 'little') + 1).to_bytes(2, 'little')

    if ((int.from_bytes(message[0:2],'little') - bufferBias)<windowSize):
        receiverSocket.sendto(message[0:2], senderAddress)
        buffer[int.from_bytes(message[0:2],'little') - bufferBias] = message
        print("GOT PACKET IN WINDOW, SENT ACK ", message[0:3])
    
    while (buffer[0]!=None):
        bufferBias+=1
    #   receiverSocket.sendto(message[0:2], senderAddress)
        EOF += buffer[0][2]
        data = buffer[0][3:]
        file.write(data)
        print("WROTE TO FILE ", buffer[0][0:3])
        lastPacket = buffer.pop(0)
        buffer.append(None)
        if (buffer[0] == None):
            print("HEAD OF LIST IS NONE")
        else:
            print("NEW HEAD OF BUFFER ", buffer[0][0:3])
        #prevSequenceNum = message[0:2]
    

#To make sure final ACK is recieved by sender
for i in range(20):
    receiverSocket.sendto(lastPacket[0:2], senderAddress)

receiverSocket.close()
file.close()