from socket import *
import os
import platform
import re
import _thread as thread
try:
	import httplib
except:
	import http.client as httplib

def main():
        serverPort = 23
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(1)
        print('The server is ready to receive')
        while 1:
                connectionSocket, addr = serverSocket.accept()
                thread.start_new_thread(new_client,(connectionSocket, addr))
        connectionSocket.close()

def new_client(clientSocket, addr):
	while True:
        	sentence = clientSocket.recv(1024)
        	output = ''
        	if (sentence==b"cpu"):
                	output += cpuInfo()
        	if (sentence==b"meminfo"):
                	output += memInfo()
        	if (sentence==b"memswap"):
                	output += memSwap()
        	if (sentence==b"storage"):
                	output += "Storage Memory:\n"
                	output += os.popen("df").read()
        	if (sentence==b"internet"):
                	if check_internet():
                                output+="Server Status: Online"
                	else:
                                output+="Server Status: Offline"
        	clientSocket.send(output.encode('utf-8'))
	clientSocket.close()

def check_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

def cpuInfo():
        cpuInfo = "CPU Info:\n"
        cpuInfo += "Architecture	: "+platform.architecture()[0]+"\n"
        cpuInfo += os.popen("cat /proc/cpuinfo | grep 'model name'").read()
        cpuInfo += os.popen("lscpu | grep 'cache'").read()
        cpuInfo = cpuInfo.replace("\t", "")
        return cpuInfo

def memInfo():
        memInfo = "Memory Info:\n"
        memTotal = os.popen("cat /proc/meminfo | grep 'MemTotal'").read()
        memTotal = int(re.search('\d+', memTotal).group())
        memFree = os.popen("cat /proc/meminfo | grep 'MemFree'").read()
        memFree = int(re.search('\d+', memFree).group())
        memUsed = memTotal - memFree
        memInfo += "Total Memory: " + str(memTotal) + "\n"
        memInfo += "Used Memory: " + str(memUsed) + "\n"
        memInfo += "Free Memory: " + str(memFree) + "\n"
        return memInfo

def memSwap():
        swapMem = "Swap Memory:\n" 
        swapTotal = os.popen("cat /proc/meminfo | grep 'SwapTotal'").read()
        swapTotal = int(re.search('\d+', swapTotal).group())
        swapFree = os.popen("cat /proc/meminfo | grep 'SwapFree'").read()
        swapFree = int(re.search('\d+', swapFree).group())
        swapUsed = swapTotal - swapFree
        swapMem += "Swap Total: " + str(swapTotal) + "\n"
        swapMem += "Swap Used: " + str(swapUsed) + "\n"
        swapMem += "Swap Free: " + str(swapFree) + "\n"
        return swapMem

if __name__ == '__main__':
    main()
