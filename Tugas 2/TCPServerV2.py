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
        serverPort = 8023
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
            if (b"all" in sentence):
                    fullReport = True
            else:
                    fullReport = False
            if (b"cpuinfo" in sentence) or fullReport:
                    output += cpuInfo()
            if (b"meminfo" in sentence) or fullReport:
                    output += memInfo()
            if (b"memswap" in sentence) or fullReport:
                    output += memSwap()
            if (b"storage" in sentence) or fullReport:
                    output += "[STORAGE MEMORY]\n"
                    output += os.popen("df").read()
            if (b"internet" in sentence) or fullReport:
                    if check_internet():
                                output+="[SERVER STATUS: ONLINE]\n"
                    else:
                                output+="[SERVER STATUS: OFFLINE]\n"
            if (b'access' in sentence) or fullReport:
                    output += serverAccess()
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
        cpuInfo = "[CPU INFO]\n"
        cpuInfo += "Architecture    : "+platform.architecture()[0]+"\n"
        cpuInfo += os.popen("cat /proc/cpuinfo | grep 'model name'").read()
        l1_cache = os.popen("lscpu | grep 'L1'").read().split("\n")
        cpuInfo += "L1d cache: " + l1_cache[0].split(" ")[-1] + "\n"
        cpuInfo += "L1i cache: " + l1_cache[1].split(" ")[-1] + "\n"
        l2_cache = os.popen("lscpu | grep 'L2'").read().split(" ")
        cpuInfo += "L2 cache: " + l2_cache[-1]
        l3_cache = os.popen("lscpu | grep 'L3'").read().split(" ")
        cpuInfo += "L3 cache: " + l3_cache[-1]
        cpuInfo = cpuInfo.replace("\t", "")
        return cpuInfo

def memInfo():
        memInfo = "[PHYSICAL MEMORY INFO]\n"
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
        swapMem = "[SWAP MEMORY INFO]\n" 
        swapTotal = os.popen("cat /proc/meminfo | grep 'SwapTotal'").read()
        swapTotal = int(re.search('\d+', swapTotal).group())
        swapFree = os.popen("cat /proc/meminfo | grep 'SwapFree'").read()
        swapFree = int(re.search('\d+', swapFree).group())
        swapUsed = swapTotal - swapFree
        swapMem += "Swap Total: " + str(swapTotal) + "\n"
        swapMem += "Swap Used: " + str(swapUsed) + "\n"
        swapMem += "Swap Free: " + str(swapFree) + "\n"
        return swapMem

def serverAccess():
        serverAccess = "[SUCCESSFUL SERVER ACCESS]\n"
        successfulUser = os.popen("last").read().split("\n")
        for i in range(0,10):
            if i < len(successfulUser):
                serverAccess += successfulUser[i]+"\n"
        serverAccess += "[FAILED SERVER ACCESS]\n"
        failedUser = os.popen("lastb").read().split("\n")
        for i in range(0,10):
            if i < len(failedUser):
                serverAccess += failedUser[i]+"\n"
        return serverAccess

if __name__ == '__main__':
    main()

