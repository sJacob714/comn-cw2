from cmath import inf
from socket import *
import sys

def main(receiverPort, fileName):

    receiverSocket = socket(AF_INET, SOCK_DGRAM)
    receiverSocket.bind(('', receiverPort))
    file = open(fileName, "wb")

    #print("The receiver is ready to recieve")
    EOF = 0
    # loops until end of file is received
    while (EOF==0):
        message, senderAddress = receiverSocket.recvfrom(1027)
        EOF = message[2]
        data = message[3:]
        file.write(data)

    receiverSocket.close()
    file.close()

if __name__ == "__main__":
    receiverPort = int(sys.argv[1])
    fileName = str(sys.argv[2])

    main(receiverPort, fileName)