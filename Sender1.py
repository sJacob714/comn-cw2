from socket import *
import sys
import time

receiverName = str(sys.argv[1])
receiverPort = int(sys.argv[2])
fileName = str(sys.argv[3])

file = open(fileName, 'rb')
senderSocket = socket(AF_INET, SOCK_DGRAM)
sequenceNum = 0

while (len(file.peek())!=0):
    fileBytes = file.read(1024)

    if len(file.peek())!=0:
        EOF = 0
    else:
        EOF = 255

    packet = sequenceNum.to_bytes(2, 'little')  + EOF.to_bytes(1, 'little') + fileBytes
    senderSocket.sendto(packet, (receiverName, receiverPort))
    sequenceNum+=1
    time.sleep(0.005)
    
file.close()
senderSocket.close()