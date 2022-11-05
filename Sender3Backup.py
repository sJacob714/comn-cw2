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

retransmissions = 0

lastAcknowledged = [-1,-1]
start = time.time()
while (len(packetList)>0):
    #print(len(packetList))
    for numSent in range(min(windowSize,len(packetList))):
        senderSocket.sendto(packetList[-numSent-1], (receiverName, receiverPort))
        #time.sleep(0.005)
        print("sent ", packetList[-numSent-1][0:3])
    numSent+=1
    #print("NUMBER SENT" ,numSent)
    packetsAcknowledged = 0
    reSendPackets = False

    #while keepWaiting and numSent>0:
    while (not reSendPackets) and (packetsAcknowledged<numSent):
        try:
            #start = time.time()
            ack, receiverAddress = senderSocket.recvfrom(2)
            #print("time taken :", time.time()-start)
            #if (ack == lastAcknowledged[0:2]):
            if (int.from_bytes(ack, 'little') < int.from_bytes(packetList[-1][0:2],'little')):
                print("RECEIVED PREVIOUS ACKNOWLEDGEMENT ", lastAcknowledged[0:2])
                #senderSocket.sendto(packetList[i], (receiverName, receiverPort))
                #reSendPackets = True
                retransmissions+=min(windowSize, len(packetList))
                continue
            ##print(ack," here ",packetList[0][0:3])
            print("Ack for ", ack)
            ##print("Previous Ack ", lastAcknowledged[0:2])
            while ack!=packetList[-1][0:2]:
                ##print(ack," here ",packetList[0][0:3])
                #print("not found, list before pop ", packetList[0][0:3])
                packetList.pop()
                #print("after pop ", packetList[0][0:3])
                ##print(len(packetList))
                packetsAcknowledged+=1
            #print("found, list before pop ", packetList[0][0:3])
            lastAcknowledged = packetList.pop()
            packetsAcknowledged+=1
            #print("after pop ", packetList[0][0:3])
            #print("NUMBER OF PACKETS ACKNOWLEDGED ", packetsAcknowledged)
        except:
            print("TIMED OUT")
            retransmissions+=min(windowSize, len(packetList))
            reSendPackets = True
print()
print("time taken: ", time.time()-start)
print("number of packets ", sequenceNum)
print("number of retransmissions ", retransmissions-874)


file.close()
senderSocket.close()