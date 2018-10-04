from socket import *
import argparse

serverName = 'localhost'
serverPort = 23
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

parser = argparse.ArgumentParser(description="List of server command")
parser.add_argument('-all', help='Get all server information', action='store_const', const='all')
parser.add_argument('-c', help="Get server cpu info", action='store_const', const='cpuinfo')
parser.add_argument('-m', help='Get server physical memory info', action='store_const', const='meminfo')
parser.add_argument('-sm', help='Get server virtual memory info', action='store_const', const='memswap')
parser.add_argument('-st', help='Get server file storage info', action='store_const', const='storage')
parser.add_argument('-i', help="Get server internet connection status", action='store_const', const='internet')
parser.add_argument('-acc', help="Show listing of last logged in users", action='store_const', const='access') 
args = parser.parse_args()
request = ''
for key, value in vars(args).items():
    if isinstance(value, str):
        request += value + ' '

clientSocket.send(request.encode('utf-8'))
modifiedSentence = clientSocket.recv(4096)
print (modifiedSentence.decode('utf-8'))
clientSocket.close()

