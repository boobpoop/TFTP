#!/usr/bin/env python
# coding=utf-8
import struct
from socket import *
from threading import Thread

#定义下载的线程
def download(fileName, user_ip, user_port):
	#print(fileName, user_ip, user_port)
	#创建一个新的socket，用来向客户端发送数据，同时，不绑定端口，默认新socket就是随机端口
	s_download = socket(AF_INET, SOCK_DGRAM)
	#num为发送的每个block号
	num = 0
	#try-except相当于if-else
	try:
		#指定下载的路径
		f1 = open("E:\\CloudMusic\\"+fileName , "rb")
	except:
		#若文件不存在，放客户端发送error消息，服务器端也要显示
		errorData = struct.pack("!HHHb", 5, 5, 5, num)
		s_download.sendto(errorData, (user_ip, user_port))
		print("file doesn't exist")
		exit()
	
	while True:
		readData = f1.read(512)
		#readData本身就是二进制，因为读取的时候是以"rb"的形式。因此把pack数据和readData数据相连接
		sendData = struct.pack("!HH", 3, num) + readData
		#收到下载请求后直接放客户端发送数据。
		s_download.sendto(sendData, (user_ip, user_port))
		#接收ACK消息
		ACK = s_download.recvfrom(1024)
		#print(ACK)
		opCode, blockNum = struct.unpack("!HH", ACK[0])
		#print(opCode, blockNum)
		if opCode == 4 and blockNum == num:
			num += 1
			if len(readData) < 512:
			print("success")
			f1.close()
			s_download.close()
			exit()

def upload(fileName, user_ip, user_port):
	#print(fileName, user_ip, user_port)
	#新建一个socket，用于传输用户上传的数据
	s_upload = socket(AF_INET, SOCK_DGRAM)
	num = 0
	f1 = open("E:\\CloudMusic\\"+fileName , "ab")
	#向客户端发送ACK，表示已经收到了上传请求
	ACK_data = struct.pack("!HH", 4, 0)
	s_upload.sendto(ACK_data, (user_ip, user_port))
	while True:
		#接收用户上传的数据
		recvData = s_upload.recvfrom(1024)
		#print(recvData)
		opCode, blockNum = struct.unpack("!HH", recvData[0][:4])
		if opCode == 3 and blockNum == num:
			f1.write(recvData[0][4:])
			ACK = struct.pack("!HH", 4, num)
			s_upload.sendto(ACK, (user_ip, user_port))
			if len(recvData[0]) < 516:
				print("success")
				f1.close()
				s_upload.close()
				exit()
		num += 1
		
def main():
	#新建一个socket，用于接收用户的上传或下载请求
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(("192.168.114.1", 69))    
    recv_Data, (user_ip, user_port) = udpSocket.recvfrom(1024)
    #print(recvData)
    opCode = struct.unpack("!H", recv_Data[:2])
    fileName = recv_Data[2:-7].decode("gb2312")
    #struct.unpack 不会解码二进制数据，因此str1此时还是二进制的字符串
    num1, str1, num2 = struct.unpack("!b5sb", recv_Data[-7:]) 
    #print(opCode, fileName)
	#print(num1)
	#print(str1)
	#print(num2)
	#若(0, "octet", 0) 正确,才会执行下载和上传,否则不符合tftp协议。
    if num1 == 0 and str1 == "octet".encode("gb2312") and num2 == 0:
		#创建两个线程，一个线程进行下载，一个线程进行上传
        if opCode[0] == 1:
            th1 = Thread(target = download, args = (fileName, user_ip, user_port))
            th1.start()
        elif opCode[0] == 2:
            th2 = Thread(target = upload, args = (fileName, user_ip, user_port))
            th2.start()
		#操作码只能是1或者2
        else:
            print("操作码有误")
            exit()
    else:
        print("不符合协议")
        exit()

if __name__ == "__main__":
	main()