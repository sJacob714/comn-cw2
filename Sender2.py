from socket import *
import sys
import time

receiverName = str(sys.argv[1])
receiverPort = int(sys.argv[2])
fileName = str(sys.argv[3])
retryTimeOut = int(sys.argv[4])

file = open(fileName, 'rb')
senderSocket = socket(AF_INET, SOCK_DGRAM)
senderSocket.settimeout(retryTimeOut/1000)

retransmissionNum = 0
sequenceNum = 0
while (len(file.peek())!=0):
    fileBytes = file.read(1024)
    if len(file.peek())!=0:
        EOF = 0
    else:
        EOF = 255
    packet = sequenceNum.to_bytes(2, 'little')  + EOF.to_bytes(1, 'little') + fileBytes

    if (sequenceNum==0):
        startTime = time.time()
    senderSocket.sendto(packet, (receiverName, receiverPort))
    stopAndWait = True
    while stopAndWait:
        try:
            response, receiverAddress = senderSocket.recvfrom(2)
            if (int.from_bytes(response, 'little') == sequenceNum):
                stopAndWait = False
        except:
            senderSocket.sendto(packet, (receiverName, receiverPort))
            retransmissionNum+=1

    duration = time.time()-startTime
    sequenceNum+=1
    size = (sequenceNum-1)*1024+len(fileBytes)
    #time.sleep(0.01)

#actual output
print(retransmissionNum, " ", size/duration)

#TODO REMOVE THESE OUTPUTS
print("retransmissionnum: ", retransmissionNum, " average num of retransmission: ", retransmissionNum/sequenceNum, " throughput ", size/duration, " size ", size, " time ", duration)

file.close()
senderSocket.close()