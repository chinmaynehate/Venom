from socket import *
import threading
import time

class Server:

	def __init__(self):
		self.HOST = ''
		self.PORT = 21566
		self.BUFSIZE = 1024
		self.storedData = ""
		self.CurrentData = ""
		self.messageQueueLength = 0

		self.setConnectionParams()

	def setPort(self,PORT):
		self.PORT = PORT
		self.setConnectionParams()
		


	def setConnectionParams(self):
		self.ADDR = (self.HOST,self.PORT)
		self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
		self.tcpSerSock.bind(self.ADDR)
		self.tcpSerSock.listen(self.messageQueueLength)



	def start(self):
		print("Starting Server...")
		t1 = threading.Thread(target=self.Looper)
		t1.start()
		print("Server Started.")
	


	def Looper(self):
		while True:
			# print ('Waiting for connection')
			tcpCliSock,addr = self.tcpSerSock.accept()
			# print ('...connected from :', addr)
			try:
				while True:
						data = ''
						data = tcpCliSock.recv(self.BUFSIZE)
						if not data:
								break
						else:
							# print("Data Received:",data)
							self.storedData=data.decode()
			except KeyboardInterrupt:
				break
			
		self.tcpSerSock.close()

	def getIncommignData(self):
		return self.storedData


	# Call this Function to Get the Actual Angle,Force Input
	def getInput(self):
		incomming_data = self.getIncommignData()
		return self.ParseData(incomming_data)

	def ParseData(self,data):
		data = data.split(",")
		if(data[0] !=''):
			try:
				force = float(data[0])
				angle = float(data[1])
				return angle,force
			except:
				pass
		return [0,0]




# def loopInput():
# 	while True:
# 			# print ('Waiting for connection')
# 			tcpCliSock,addr = tcpSerSock.accept()
# 			# print ('...connected from :', addr)
# 			try:
# 					global Sdata
# 					while True:
# 							data = ''
# 							data = tcpCliSock.recv(BUFSIZE)
# 							if not data:
# 									break
# 							else:
# 								# print("Data Received:",data)
# 								Sdata=data.decode()
# 			except KeyboardInterrupt:
# 					pass

# 	tcpSerSock.close();

# def printData():
# 	global Sdata
# 	global PData
# 	while True:
# 		time.sleep(0.5)
# 		if PData !=Sdata:
# 			print("Requested Data",Sdata)
# 			PData=Sdata
# 		else:
# 			pass

# def getInput():
# 	data = Sdata.split(",")
# 	if(data[0] !=''):
# 		force = float(data[0])
# 		angle = float(data[1])
# 		return angle,force
# 	else:
# 		return [0,0]


if __name__=="__main__":
	server = Server()
	server.start()

	while True:
		time.sleep(1)
		print(server.getInput())
