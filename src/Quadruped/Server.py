from socket import *
import threading


HOST = ''
PORT = 21565
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
# tcpSerSock.listen(5)
tcpSerSock.listen(0)



Sdata = ""

def init():
	pass

def getInput():
	while True:
			# print ('Waiting for connection')
			tcpCliSock,addr = tcpSerSock.accept()
			# print ('...connected from :', addr)
			try:
					while True:
							data = ''
							data = tcpCliSock.recv(BUFSIZE)
							if not data:
									break
							else:
								print("Data Received:",data)
								Sdata=data
			except KeyboardInterrupt:
					pass

	tcpSerSock.close();

def printData():
	PData = ""
	while True:
		if PData !=Sdata:
			print(Sdata)
			PData=Sdata
		else:
			pass


if __name__=="__main__":
	t1 = threading.Thread(target=getInput)
	t2 = threading.Thread(target=printData)
	t1.start()
	t2.start()


