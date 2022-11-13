from socket import *
import sys
import time


# Reads file, stores in packets of 1024 bytes chunks, adds header to each packet
def readFile(fileName):
    file = open(fileName, 'rb')
    sequenceNum = 0
    packetList = []
    while (len(file.peek())>0):
        fileBytes = file.read(1024)
        if len(file.peek())>0:
            EOF = 0
        else:
            EOF = 255
        packetList.append( (sequenceNum.to_bytes(2, 'little')  + EOF.to_bytes(1, 'little') + fileBytes) )
        sequenceNum+=1
    file.close()
    return packetList

def main(receiverName, receiverPort, fileName):

    packetList = readFile(fileName)
    senderSocket = socket(AF_INET, SOCK_DGRAM)

    # sends all packets to receiver
    for packet in packetList:
        senderSocket.sendto(packet, (receiverName, receiverPort))
        time.sleep(0.005)
    senderSocket.close()

if __name__ == "__main__":
    receiverName = str(sys.argv[1])
    receiverPort = int(sys.argv[2])
    fileName = str(sys.argv[3])

    main(receiverName, receiverPort, fileName)