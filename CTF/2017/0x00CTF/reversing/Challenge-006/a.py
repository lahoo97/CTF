#!/usr/bin/python

v8 = 1
v9 = 0
v11 = [0]*6
v10 = [3,7,1,1,7,3]
byte_601060 = [1,2,1,3,2,5,0,0,0,0,0,0,0,0,0,0]

for count in range (0,6):
	v11[count] = byte_601060[(count+3)^6] * v10[(count+2)%6] ^ v10[count]
	v9 += v8 * v11[count]
	v8 *= 10
print v9

