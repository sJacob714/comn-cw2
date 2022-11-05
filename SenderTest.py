from socket import *
receiverName = 'localhost'
receiverPort = 12000

senderSocket = socket(AF_INET, SOCK_DGRAM)
message = "awesome test"
senderSocket.sendto(message.encode(), (receiverName, receiverPort))
modifiedMessage, receiverAddress = senderSocket.recvfrom(2048)

print(modifiedMessage.decode())
senderSocket.close()