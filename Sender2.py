from socket import *
import sys
import time
import os

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

def main(receiverName, receiverPort, fileName, retryTimeOut):
    senderSocket = socket(AF_INET, SOCK_DGRAM)
    senderSocket.settimeout(retryTimeOut/1000)  #set timeout for socket

    packetList = readFile(fileName)

    # used for stats
    retransmissionNum = 0
    startTime = time.time()

    # itterates through packetList and sends to receiver
    for packet in packetList:
        senderSocket.sendto(packet, (receiverName, receiverPort))

        # stops and waits for Ack to be received
        stopAndWait = True
        while stopAndWait:
            try:
                # listens for ack from receiver
                response, receiverAddress = senderSocket.recvfrom(2)
                if (response == packet[0:2]):
                    stopAndWait = False
            except:
                # resends packet if socket times out
                senderSocket.sendto(packet, (receiverName, receiverPort))
                retransmissionNum+=1

    size =  os.stat(fileName).st_size
    duration = time.time()-startTime

    #actual output
    print(retransmissionNum, " ", (size/duration)/1000)

    '''
    #TODO REMOVE THESE OUTPUTS
    size = (sequenceNum-1)*1024+len(fileBytes)
    print()
    print("time taken: ", time.time()-startTime)
    print("number of packets ", sequenceNum)
    print("number of retransmissions ", retransmissionNum)
    print("Thorougput: ", size/(time.time()-startTime))
    '''

    senderSocket.close()

if __name__ == "__main__":
    receiverName = str(sys.argv[1])
    receiverPort = int(sys.argv[2])
    fileName = str(sys.argv[3])
    retryTimeOut = int(sys.argv[4])
    main(receiverName, receiverPort, fileName, retryTimeOut)