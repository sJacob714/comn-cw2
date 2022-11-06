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

# Reads file, stores in packets of 1024 bytes chunks, adds header to each packet
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

# Used for stats
start = time.time()
retransmissions = 0

windowBase = 0
# Loops until windowBase has reached end of packetList
while (windowBase < len(packetList)):

    # Sends all packets in the window
    for numSent in range( min(windowSize, (len(packetList)-windowBase)) ):
        senderSocket.sendto(packetList[windowBase + numSent], (receiverName, receiverPort))
        retransmissions+=1

    packetsAcknowledged = 0     #Tracks number of sent packets acknowledged
    reSendPackets = False
    # loops until told to resend, or all sent packets are acknowledged
    while (not reSendPackets) and (packetsAcknowledged < min(windowSize, (len(packetList)-windowBase))):
        try:
            ack, receiverAddress = senderSocket.recvfrom(2)
        
        # resends packets if socket times out
        except:
            reSendPackets = True
            continue
        
        # Ignores ack for packet before current window
        if (int.from_bytes(ack, 'little') < int.from_bytes(packetList[windowBase][0:2],'little')):
            continue

        # Shifts window forward until base is at newest acknowledged packet
        while ack!=packetList[windowBase][0:2]:
            windowBase+=1
            packetsAcknowledged+=1
        # Shifts window once more to get to oldest unacknowledged packet
        windowBase+=1
        packetsAcknowledged+=1

#ACTUAL OUTPUT
size = (sequenceNum-1)*1024+len(fileBytes)
print( (size/(time.time()-start))/1000 )

#TODO: STATS DELETE THIS
print()
print("time taken: ", time.time()-start)
print("number of packets ", sequenceNum)
print("number of retransmissions ", retransmissions-sequenceNum)
print("Thorougput: ", size/(time.time()-start))


file.close()
senderSocket.close()