from socket import *
receiverPort = 12000

receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind(('', receiverPort))
print("The receiver is ready to recieve")
while True:
    message, senderAddress = receiverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print(message.decode())
    print("The receiver is ready to recieve")
    receiverSocket.sendto(modifiedMessage.encode(), senderAddress)