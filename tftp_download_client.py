from socket import *
import struct
#下载客户端跟服务器的下载线程类似
def download():
	udpSocket = socket(AF_INET, SOCK_DGRAM)
	udpSocket.bind(("192.168.114.132", 9000))
	ip = input("please input ipaddress destination:")
	port = int(input("please input port:"))
	fileName = input("please input file:")
	sendData = struct.pack("!H%dsb5sb" %len(fileName), 1, fileName.encode("gb2312"), 0, "octet".encode("gb2312"), 0)
	udpSocket.sendto(sendData, (ip, port))
	f1 = open(fileName, "ab") #以二进制形式写文件
	i = 0
	while True:
	    recvData = udpSocket.recvfrom(2000)
	    #print(recvData)
	    data,sock = recvData
	    #print(data)
	    #print(sock)
	    #print(len(data))
	    opCode, blockNum = struct.unpack("!HH", data[0:4])
	    #print(op)
	    #print(block)
	    if opCode == 3: 
	        ACK = struct.pack("!HH", 4, blockNum)
	        udpSocket.sendto(ACK, (sock[0], sock[1]))
	    if opCode == 5:
	        print("the file doesn't exist!!!")
	        break
	    f1.write(data[4:])
	    if len(data) < 516:
	        print("结束")
	        break
	f1.close()
	udpSocket.close()

if __name__ == "__main__":
	download()
