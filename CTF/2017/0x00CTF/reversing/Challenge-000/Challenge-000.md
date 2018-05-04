Challenge-000(guessme)
======================
##### 50 point
-----------------
## Description
```
Hi there. Can you find the right key that unlocks the flag?

Platform: 64 bit Linux (developed on Ubuntu)
```

## 풀이
```
Enter a key: asdf
FAIL
```
guessme라는 파일을 실행해보면 Enter a key: 라는 문구가 뜨고 아무거나 입력하면 FAIL이라는 문구가 뜬다.
이 문제는 key를 찾는 것이 핵심인 것 같다.
IDA x64를 통해서 Enter a key라는 문구를 검색해서 프로그램의 흐름을 잡았다.
```C
loc_40101E:             ; "Good key!\n"
mov     esi, offset aGoodKey
mov     edi, offset _ZSt4cout ; std::cout
call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
//std:cout를 offset으로 선언을 하는 것으로 봐서 프린트 해주는 함수로 추측
mov     esi, offset aTheFlagIs0x00c ; "The flag is: 0x00CTF{"
mov     edi, offset _ZSt4cout ; std::cout
call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
//std:cout를 offset으로 선언을 하는 것으로 봐서 프린트 해주는 함수로 추측
mov     rdx, rax
lea     rax, [rbp+var_40]
mov     rsi, rax
mov     rdi, rdx
call    __ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKNSt7__cxx1112basic_stringIS4_S5_T1_EE ; std::operator<<<char,std::char_traits<char>,std::allocator<char>>(std::basic_ostream<char,std::char_traits<char>> &,std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>> const&)
//???
mov     esi, offset asc_401C55 ; "}\n"
mov     rdi, rax
call    __ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc ; std::operator<<<std::char_traits<char>>(std::basic_ostream<char,std::char_traits<char>> &,char const*)
//???
mov     ebx, 0
```
분석 결과 "Good key!"라는 문구와 함께 "The flag is: 0x00CTF{"라는 문구와 "}"라는 문구가 나온다.
```
lea     rax, [rbp+var_40]
mov     rsi, rax
mov     rdi, rdx
call    __ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKNSt7__cxx1112basic_stringIS4_S5_T1_EE ; std::operator<<<char,std::char_traits<char>,std::allocator<char>>(std::basic_ostream<char,std::char_traits<char>> &,std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>> const&)
```
따라서 키값은 [rbp+var_40]이라는 곳에 저장 될 것이다.
```
.text:0000000000400F51 loc_400F51:
.text:0000000000400F51 lea     rax, [rbp+var_40]
.text:0000000000400F55 mov     rdi, rax
.text:0000000000400F58 call    __ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(void)
//[rbp+var_40] 입력받은 문자열 길이 체크
.text:0000000000400F5D mov     rbx, rax
.text:0000000000400F60 lea     rax, [rbp+var_60]
.text:0000000000400F64 mov     rdi, rax
.text:0000000000400F67 call    sub_401402 // 원래 문자열 길이를 체크해서 rbx에 저장
.text:0000000000400F6C cmp     rbx, rax //길이는 E
.text:0000000000400F6F setnz   al
.text:0000000000400F72 test    al, al
.text:0000000000400F74 jz      short loc_400F8F
```
첫번째 분기문에서 보면 입력한 길이를 비교한다. jz로 올바른 분기인 loc_400F8F로 가기 위해서는 al이 0이어야 한다. cmp~test까지는 cmp로 Z플래그가 0이면 setnz에서 al을 1로 세트 시키고 test 문에서 z플래그가 0이 아니게 되기 때문에 rbx와 rax는 같아야 한다. 따라서 입력하는 key는 E(14자리)이다.
```
.text:0000000000400FB8 mov     eax, [rbp+var_84]
.text:0000000000400FBE movsxd  rdx, eax
.text:0000000000400FC1 lea     rax, [rbp+var_40]
.text:0000000000400FC5 mov     rsi, rdx
.text:0000000000400FC8 mov     rdi, rax
.text:0000000000400FCB call    __ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm ; std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator[](ulong)
.text:0000000000400FD0 movzx   eax, byte ptr [rax]
.text:0000000000400FD3 movsx   eax, al
.text:0000000000400FD6 lea     ebx, [rax-61h]
.text:0000000000400FD9 mov     eax, [rbp+var_84]
.text:0000000000400FDF movsxd  rdx, eax
.text:0000000000400FE2 lea     rax, [rbp+var_60]
.text:0000000000400FE6 mov     rsi, rdx
.text:0000000000400FE9 mov     rdi, rax
.text:0000000000400FEC call    sub_4012D8
.text:0000000000400FF1 mov     eax, [rax]
.text:0000000000400FF3 cmp     ebx, eax
.text:0000000000400FF5 setnz   al
.text:0000000000400FF8 test    al, al
.text:0000000000400FFA jz      short loc_401012
```
그 후 한자리씩 문자를 비교하는 부분이고 cmp로 ebx와 eax를 비교하고 있다. rax에는 입력받은 변수와 61h를 빼서 ebx에 저장한다. movzx   eax, byte ptr [rax] ~ call    sub_4012D8까지 동작하면 힙영역의 주소가 rax에 저장된다. 그리고 그 힙영역의 주소는 sub_4012D8에 의해서 4byte씩 증가한다.
```
00C85C20  0000000100000000
00C85C28  0000000200000001
00C85C30  0000000500000003
00C85C38  0000000D00000008
00C85C40  0000000800000015
00C85C48  0000000B00000003
00C85C50  000000190000000E
```
따라서 키값은 61(a)를 기준으로 +0, +1, +1, +2, +3, +5, +8, +D, +15, +8, +3, +B, +E, +19이다.
```python
>>> print chr(0x61) + chr(0x61+1) + chr(0x61+1) + chr(0x61+2) + chr(0x61+3) + chr(0x61+5) + chr(0x61+8) + chr(0x61+0xD) + chr(0x61+0x15) + chr(0x61+8) + chr(0x61+3) + chr(0x61+0xB) + chr(0x61+0xE) + chr(0x61+0x19)
abbcdfinvidloz
```
```
./guessme 
Enter a key: abbcdfinvidloz
Good key!
The flag is: 0x00CTF{abbcdfinvidloz}

```
