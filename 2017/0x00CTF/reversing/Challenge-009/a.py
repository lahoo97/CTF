byte_401288 = "F4 B4 4A 3F F2 01 B7 4E 81 F6 5F 21 3D CB E7 BF D8 2A 31 BA 40 ED 39 82 A8 76 31 5E 02 3F F7 FC 70".split()
s1 = ("".join(byte_401288))+"00"
print s1

byte_4012B0 = "A7 DD 3E 4B 9B 6F D8 20 D5 9E 3A 65 52 A8 8C F0 BE 7E 59 DF 02 8C 40 D5 C9 05 45 37 6C 58 A3 95 1D 65".split()
s2 = "".join(byte_4012B0)
print s2

result = int(s1,16) ^ int(s2,16)
print hex(result)[2:70].decode("hex")

