from socket import *
import threading
import time


HOST = ''
PORT = 21578
BUFSIZE = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
# tcpSerSock.listen(5)
tcpSerSock.listen(0)



Sdata = ""
PData = ""


def init():
	pass



def loopInput():
	while True:
			# print ('Waiting for connection')
			tcpCliSock,addr = tcpSerSock.accept()
			# print ('...connected from :', addr)
			try:
					global Sdata
					while True:
							data = ''
							data = tcpCliSock.recv(BUFSIZE)
							if not data:
									break
							else:
								# print("Data Received:",data)
								Sdata=data.decode()
			except KeyboardInterrupt:
					pass

	tcpSerSock.close();

def printData():
	global Sdata
	global PData
	while True:
		time.sleep(0.5)
		if PData !=Sdata:
			print("Requested Data",Sdata)
			PData=Sdata
		else:
			pass

def getInput():
	data = Sdata.split(",")
	if(data[0] !=''):
		force = float(data[0])
		angle = float(data[1])
		return angle,force
	else:
		return [0,0]


if __name__=="__main__":
	t1 = threading.Thread(target=loopInput)
	# t2 = threading.Thread(target=printData)
	t1.start()
	# t2.start()

	while True:
		time.sleep(1.0)
		print(getInput())




