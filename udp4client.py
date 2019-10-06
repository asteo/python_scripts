import socket
host = '10.42.0.39' #'localhost'
port = 7777
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = input('Enter message to send: ')
client.sendto(msg.encode('utf-8'), (host, port))
d = client.recvfrom(1024)
reply = d[0]
addr = d[1]
print ('Server reply: ' + reply.decode('utf-8'))
client.close()