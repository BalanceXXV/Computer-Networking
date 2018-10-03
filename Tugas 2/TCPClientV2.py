from socket import *
serverName = 'localhost'
serverPort = 23
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode('utf-8'))
modifiedSentence = clientSocket.recv(1024)
print (modifiedSentence.decode('utf-8'))
clientSocket.close()
