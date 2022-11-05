from socket import *
import sys
import time

receiverName = str(sys.argv[1])
receiverPort = int(sys.argv[2])
fileName = str(sys.argv[3])
retryTimeOut = int(sys.argv[4])
windowSize = int(sys.argv[5])

file = open(fileName, 'rb')
senderSocket = socket(AF_INET, SOCK_DGRAM)
senderSocket.settimeout(retryTimeOut/1000)

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
packetList.reverse()

start = time.time()
retransmissions = 0
lastAcknowledged = [-1,-1]

while (len(packetList)>0):

    for numSent in range(min(windowSize,len(packetList))):
        senderSocket.sendto(packetList[-numSent-1], (receiverName, receiverPort))
        #print("sent ", packetList[-numSent-1][0:3])
    numSent+=1

    packetsAcknowledged = 0
    reSendPackets = False
    while (not reSendPackets) and (packetsAcknowledged<numSent):

        try:
            ack, receiverAddress = senderSocket.recvfrom(2)

            if (int.from_bytes(ack, 'little') < int.from_bytes(packetList[-1][0:2],'little')):
                #print("RECEIVED PREVIOUS ACKNOWLEDGEMENT ", lastAcknowledged[0:2])
                retransmissions+=1
                continue

            #print("Ack for ", ack)
            while ack!=packetList[-1][0:2]:
                packetList.pop()
                packetsAcknowledged+=1
            lastAcknowledged = packetList.pop()
            packetsAcknowledged+=1

        except:
            #print("TIMED OUT")
            retransmissions+=1
            reSendPackets = True

print()
print("time taken: ", time.time()-start)
print("number of packets ", sequenceNum)
print("number of retransmissions ", retransmissions)


file.close()
senderSocket.close()