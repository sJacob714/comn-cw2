from socket import *
import sys


def main(receiverPort, fileName):
    receiverSocket = socket(AF_INET, SOCK_DGRAM)
    receiverSocket.bind(('', receiverPort))
    file = open(fileName, "wb")

    EOF = 0
    lastAckSequenceNum = -1    # Used to resend acks
    expectedSequenceNum = 0    
    expectedSequenceNum = expectedSequenceNum.to_bytes(2, 'little')

    #print("The receiver is ready to recieve")
    # Until End of file is received
    while EOF==0:
        message, senderAddress = receiverSocket.recvfrom(1027)

        # if message is not next in sequence, sends Ack for last correctly received message and ignores
        if (message[0:2]!=expectedSequenceNum):
            if lastAckSequenceNum!=-1:
                receiverSocket.sendto(lastAckSequenceNum, senderAddress)
            continue

        # if correct message, sends ack and saves data
        receiverSocket.sendto(message[0:2], senderAddress)
        EOF = message[2]
        data = message[3:]
        file.write(data)

        # calculates next expected sequence number
        expectedSequenceNum = (int.from_bytes(message[0:2], 'little') + 1).to_bytes(2, 'little')   
        #saves last acknowledged packet
        lastAckSequenceNum = message[0:2]

    #To make sure final ACK is recieved by sender
    for i in range(20):
        receiverSocket.sendto(message[0:2], senderAddress)

    receiverSocket.close()
    file.close()

if __name__ == "__main__":
    receiverPort = int(sys.argv[1])
    fileName = str(sys.argv[2])
    main(receiverPort, fileName)