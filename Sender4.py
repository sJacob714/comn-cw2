from socket import *
from cmath import inf
import sys
import time

receiverName = str(sys.argv[1])
receiverPort = int(sys.argv[2])
fileName = str(sys.argv[3])
retryTimeOut = int(sys.argv[4])/1000
windowSize = int(sys.argv[5])

file = open(fileName, 'rb')
senderSocket = socket(AF_INET, SOCK_DGRAM)
#senderSocket.settimeout(retryTimeOut/1000)
senderSocket.setblocking(False)

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
#packetList.reverse()

timerList = []
retransmissions = 0
lastAcknowledged = [-1,-1]
numSent = 0
windowBase = 0

while (windowBase<len(packetList)):
    #print("At start")

    while numSent<min(windowSize,len(packetList)-windowBase):
    #for numsent in range(min(windowSize, len(packetList))):
        senderSocket.sendto(packetList[windowBase + numSent], (receiverName, receiverPort))
        timerList.append(time.time())
        print("sent ", packetList[windowBase + numSent][0:3])
        numSent+=1
        

    packetsAcknowledged = 0
    listening = True
    #while (listening) and (packetsAcknowledged<numSent):
    while listening:
        #print("at listening")
        #print(windowBase)
        #print(len(packetList))

        try:
            #print("at recieve")
            ack, receiverAddress = senderSocket.recvfrom(2)

            '''
            if (int.from_bytes(ack, 'little') < int.from_bytes(packetList[-1][0:2],'little')):
                #print("RECEIVED PREVIOUS ACKNOWLEDGEMENT ", lastAcknowledged[0:2])
                retransmissions+=1
                continue
            '''

            print("Ack for ", ack)
            timerList[int.from_bytes(ack, 'little')] = inf


            while timerList[windowBase]==inf:
                print("PREVIOUS WINDOW HEAD ", packetList[windowBase][0:3], "TIMER ", timerList[windowBase])
                windowBase+=1
                print(windowBase)
                print(len(packetList))
                print(len(timerList))
                #print("NEW WINDOW HEAD ", packetList[windowBase][0:3], "TIMER ", timerList[windowBase])
                #print(windowBase)
                #print(len(packetList))
                numSent-=1
                if (windowBase==len(packetList)):
                    break
            listening = False
                #packetsAcknowledged+=1
            #lastAcknowledged = packetList.pop()
            #packetsAcknowledged+=1

        except:
            #print("TIMED OUT")
            if (windowBase==len(timerList)):
                listening = False
            for i in range(windowBase, len(timerList)):
                #print((time.time()-timerList[i]))
                if ( (time.time()-timerList[i]) > retryTimeOut):
                    senderSocket.sendto(packetList[i], (receiverName, receiverPort))
                    print("TIMED OUT RESENT ", packetList[i][0:3])
                    timerList[i] = time.time()
            #retransmissions+=1

#print()
#print("time taken: ", time.time()-start)
#print("number of packets ", sequenceNum)
#print("number of retransmissions ", retransmissions)


file.close()
senderSocket.close()