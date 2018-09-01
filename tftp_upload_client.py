#!/usr/bin/env python
# coding=utf-8
import struct
from socket import *
#上传客户端跟服务器的上传线程类似
def upload():
	udpSocket = socket(AF_INET, SOCK_DGRAM)
	udpSocket.bind(("192.168.114.132", 9000))

	fileName = input("please input the file name you what to upload:")
	ip = input("please input the ipaddress destination:")
	port = 69

	uploadRequest = struct.pack("!H%dsb5sb" %len(fileName), 2, fileName.encode("gb2312"), 0, "octet".encode("gb2312"), 0)
	udpSocket.sendto(uploadRequest, (ip, port))
	recvData = udpSocket.recvfrom(516)
	opCode, blockNum = struct.unpack("!HH", recvData[0][:4])
	newPort = recvData[1][1]
	print(newPort)
	if opCode != 4:
	    print("error occurs")
	    return 
	else:
	    f1 = open(fileName, "rb")
	num = 0
	while True:
	    readData = f1.read(512)
	    sendData = struct.pack("!HH" ,3 , num) + readData
	    udpSocket.sendto(sendData, (ip, newPort))
	    recv = udpSocket.recvfrom(1024)
	    #print(recv)
	    operCode, blockNummber = struct.unpack("!HH", recv[0][:4]) 
	    if len(sendData) == 516 and operCode == 4 and blockNummber == num:
	        num += 1
	    else:
	        print("upload success")
	        break
	f1.close()
	udpSocket.close()

if __name__ == "__main__":
	upload()
