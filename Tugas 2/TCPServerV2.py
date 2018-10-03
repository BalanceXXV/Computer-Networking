from socket import *
import os
import platform
import re

def internet(host="8.8.8.8", port=53, timeout=3):
        try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                return True
        except:
                return False


serverPort = 23
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while 1:
     connectionSocket, addr = serverSocket.accept()
     sentence = connectionSocket.recv(1024)
     output = ''
     if (sentence==b"cpu"):
          output += "CPU Info:\n"
          output = "Architecture	: "+platform.architecture()[0]+"\n"
          output += os.popen("cat /proc/cpuinfo | grep 'model name'").read()
          output += os.popen("lscpu | grep 'cache'").read()
          output = output.replace("\t", "")
          output = output.encode('utf-8')
     if (sentence==b"meminfo"):
          output += "Memory Info:\n"
          memTotal = os.popen("cat /proc/meminfo | grep 'MemTotal'").read()
          memTotal = int(re.search('\d+', memTotal).group())
          memFree = os.popen("cat /proc/meminfo | grep 'MemFree'").read()
          memFree = int(re.search('\d+', memFree).group())
          memUsed = memTotal - memFree
          output = "Total Memory: " + str(memTotal) + "\n"
          output += "Used Memory: " + str(memUsed) + "\n"
          output += "Free Memory: " + str(memFree) + "\n"
          output = output.encode('utf-8')
     if (sentence==b"memswap"):
          output += "Swap Memory:\n" 
          swapTotal = os.popen("cat /proc/meminfo | grep 'SwapTotal'").read()
          swapTotal = int(re.search('\d+', swapTotal).group())
          swapFree = os.popen("cat /proc/meminfo | grep 'SwapFree'").read()
          swapFree = int(re.search('\d+', swapFree).group())
          swapUsed = swapTotal - swapFree
          output += "Swap Total: " + str(swapTotal) + "\n"
          output += "Swap Used: " + str(swapUsed) + "\n"
          output += "Swap Free: " + str(swapFree) + "\n"
          output = output.encode('utf-8')
     if (sentence==b"storage"):
          output += "Storage Memory:\n"
          output += os.popen("df").read()
          output = output.encode('utf-8')
     if (sentence==b"internet"):
          print(internet())
          if internet():
               output+="Server Status: Online"
          else:
               output+="Server Status: Offline"
          output = output.encode('utf-8')
     connectionSocket.send(output)
     connectionSocket.close()
