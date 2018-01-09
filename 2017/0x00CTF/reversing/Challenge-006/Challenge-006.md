Challenge-004
======================

-----------------
## Description
```
004
```

## 풀이
```
Shuffled Love
by p1c0

My PIN is 371173
Your PIN:
```
c1을 실행하면 다음과 같이 나온다. 그리고 아무값이나 넣어보면 "Oh. You are not the one :(."이라는 문구가 나온다.
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v4; // [sp+4h] [bp-Ch]@1
  int v5; // [sp+8h] [bp-8h]@1
  int v6; // [sp+Ch] [bp-4h]@1

  v4 = 0;
  v6 = 0;
  puts("Shuffled Love");
  puts("by p1c0\n");
  v5 = 371173;
  printf("My PIN is %d\nYour PIN:", 371173LL);
  __isoc99_scanf(4196678LL, &v4);
  v6 = sub_40069D(v5, v4);
  if ( v6 )
    puts("Oh. You are not the one :(.");
  else
    printf("You read my mind!!!. We are twin souls\n--> 0x00CTF{Y0uR_th3_0n3_%x} <--\n\n", (unsigned int)v4);
  return 0;
}
```

ida로 분석을 해보면 v6에 0이면 else가 실행이 되면서 플래그 값이 나온다. 입력한 값을 v4에, 371173을 v5에 각각 저장하고 sub_40069D를 호출한다.
```
__int64 __fastcall sub_40069D(signed int a1, int a2)
{
  __int64 result; // rax@7
  __int64 v3; // rbx@7
  signed int orgin; // [sp+Ch] [bp-44h]@1
  signed int count; // [sp+14h] [bp-3Ch]@1
  signed int counta; // [sp+14h] [bp-3Ch]@4
  signed int v7; // [sp+18h] [bp-38h]@1
  signed int v8; // [sp+18h] [bp-38h]@4
  unsigned int v9; // [sp+1Ch] [bp-34h]@1
  char v10[16]; // [sp+20h] [bp-30h]@2
  char v11[8]; // [sp+30h] [bp-20h]@5
  __int64 v12; // [sp+38h] [bp-18h]@1

  origin = a1;									// 371173
  v12 = *MK_FP(__FS__, 40LL);
  v7 = 100000;
  v9 = 0;
  for ( count = 0; count <= 5; ++count )
  {
    v10[count] = origin / v7;
    origin -= v7 * v10[count];
    v7 /= 10;
  }												// v10[count]에 각 자리 저장
  putchar(10);
  v8 = 1;
  for ( counta = 0; counta <= 5; ++counta )
  {
    v11[counta] = byte_601060[(signed __int64)((counta + 3) ^ 6)] * v10[(counta + 2) % 6] ^ v10[counta];							//byte_601060[] = "121325"
    v9 += v8 * v11[counta];
    v8 *= 10;
  }												// v9연산
  result = a2 ^ v9;
  v3 = *MK_FP(__FS__, 40LL) ^ v12;
  return result;
  // result가 0이어야 else로 가기 때문에 입력값 a2 = v9어야함.
}
```
첫번째 for문에서 숫자를 v10배열에 저장하고 두번째 for문에서 연산해서 숫자 v9를 도출한다.
이때 위에서 else 구문으로 빠져야만 문제가 풀리므로 result값은 0이어야 한다. 따라서 입력값인 a2는 v9와 같아야 한다.

```python
# a.py
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
--------------------------------------------------------------------------
>>> v9 = 314066
```
314066을 pin번호로 넣으면 문제가 풀린다.
```
./a.py | ./c1
Shuffled Love
by p1c0

My PIN is 371173
Your PIN:
You read my mind!!!. We are twin souls
--> 0x00CTF{Y0uR_th3_0n3_4cad2} <--
```
