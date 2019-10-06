import socket
timeout = 60
host = 'localhost'
port = 7777
addr = (host, port)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(addr)
while True:
	print ('Waiting for data ({0} seconds)...'.format(timeout))
	server.settimeout(timeout)
	try:
		d = server.recvfrom(1024)
	except socket.timeout: 
		print('Time is out. {0} seconds have passed'.format(timeout))
		break
	received = d[0]
	addr = d[1]
	print ('Received data: ' , received)
	print ('From: ' , addr)
	msg = input('Enter message to send: ')
	server.sendto(msg.encode('utf-8'), addr)
server.close()