from socket import *
from cmath import inf
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


def main(receiverName, receiverPort, fileName, retryTimeOut, windowSize):
    retryTimeOut = retryTimeOut/1000
    senderSocket = socket(AF_INET, SOCK_DGRAM)
    senderSocket.setblocking(False)

    packetList = readFile(fileName)

    timerList = []  # stores start times of sent packets, set to inf if packet is acknowledged
    numSent = 0     # number of unacknowledged sent packets
    windowBase = 0  # Keeps track of start of window

    #TODO: STATS DELETE LATER
    start = time.time()
    retransmissions = 0

    # itterates until windowBase is at end of packetList
    while (windowBase<len(packetList)):

        # Sends any untransmitted packets within window
        while numSent<min(windowSize,len(packetList)-windowBase):
            senderSocket.sendto(packetList[windowBase + numSent], (receiverName, receiverPort))
            timerList.append(time.time())   # stores start time of sent packet
            numSent+=1
            
        listening = True
        while listening:

            try:
                ack, receiverAddress = senderSocket.recvfrom(2)     
                timerList[int.from_bytes(ack, 'little')] = inf      

            # if no ACK is received
            except:
                # loop through sent packet timers, check for timeout, and resend packet if needed
                for i in range(windowBase, len(timerList)):
                    if ( (time.time()-timerList[i]) > retryTimeOut):
                        senderSocket.sendto(packetList[i], (receiverName, receiverPort))
                        timerList[i] = time.time()      #reset timer for packet

                        retransmissions+=1  #TODO: STATS DELETE LATER
                continue

            # Increase window base and reduce num sent by 1, for every consecutive packet acknowledged
            # Moving the window along, while decreasing the size of sent packets, so in next loop, more ready packets will be sent
            while timerList[windowBase]==inf:
                windowBase+=1
                numSent-=1
                if (windowBase==len(packetList)) or (windowBase == len(timerList)):
                    break
            listening = False

    #ACTUAL OUTPUT
    size =  os.stat(fileName).st_size
    print( (size/(time.time()-start))/1000 )

    '''
    #TODO: stats delete later
    print()
    print("time taken: ", time.time()-start)
    print("number of packets ", sequenceNum)
    print("number of retransmissions ", retransmissions-sequenceNum)
    print("Thorougput: ", size/(time.time()-start))
    '''
    senderSocket.close()

if __name__ == "__main__":
    receiverName = str(sys.argv[1])
    receiverPort = int(sys.argv[2])
    fileName = str(sys.argv[3])
    retryTimeOut = int(sys.argv[4])
    windowSize = int(sys.argv[5])

    main(receiverName, receiverPort, fileName, retryTimeOut, windowSize)