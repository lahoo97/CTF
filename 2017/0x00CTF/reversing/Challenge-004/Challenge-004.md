Challenge-004
======================

-----------------
## Description
```
004
```

## 풀이
```
Welcome to the Twinlight Zone!!!
Password: asdf
Keep Trying!
-------------------------------------
Hello World!
```
hello를 실행하면 다음과 같이 나온다. 그리고 아무값이나 넣어보면 "Keep Trying!"이라는 문구가 나온다.
그러나 이 파일을 동적으로 디버깅하게 되면 "Hello World!"라는 문구가 나오고 종료가 된다. hello라는 파일에는 디버깅 유무를 확인하는 부분이 있는 듯하다. 
```
LOAD:0000000000400C40 aEsdiepwECzsLSb db 'E몖Ie뢺E*뻵뫨~}쁺Mb츋Do侶',0
LOAD:0000000000400C40                                         ; DATA XREF: LOAD:off_6020A8o
LOAD:0000000000400C62 aBxiyNR db 'B븲Y}먔',0Ah,0            ; DATA XREF: LOAD:off_6020B8o
LOAD:0000000000400C6D align 2
LOAD:0000000000400C6E word_400C6E dw 9159h                    ; DATA XREF: LOAD:off_6020C8o
LOAD:0000000000400C70 dq 44818D60B62A5A8Dh
LOAD:0000000000400C78 db 6Dh, 0C3h, 18h, 0
LOAD:0000000000400C7C ; char s[14]
LOAD:0000000000400C7C s db 'Hello World!',0Ah,0               ; DATA XREF: sub_400B62+4o
---------------------------------------------------------------------
LOAD:0000000000400A52 mov     edx, 80h                        ; n
LOAD:0000000000400A57 mov     esi, 0                          ; c
LOAD:0000000000400A5C mov     rdi, rax                        ; s
LOAD:0000000000400A5F call    memset
LOAD:0000000000400A64 lea     rax, [rbp+s]
LOAD:0000000000400A6B mov     edx, 80h                        ; nbytes
LOAD:0000000000400A70 mov     rsi, rax                        ; buf
LOAD:0000000000400A73 mov     edi, 0                          ; fd
LOAD:0000000000400A78 call    read
```
Keep Trying!이라는 문구가 검색되지 않는 것으로 볼때 문구가 암호화가 되어 있는 듯하다. 그렇지만 hello world!라는 문구로 검색했을 때 그 위에 이상한 값이 있었고 offset을 따라서 가보니 read함수로 입력 받는 부분을 찾았다. 이제 이 루틴과 hello world로 가는 루틴을 찾으면 바뀌는 이유를 알 수 있을 듯 하다. 
```
libc_2.23.so:00007FDFB90D26AE loc_7FDFB90D26AE:                       ; CODE XREF: libc_2.23.so:00007FDFB90D2796j
libc_2.23.so:00007FDFB90D26AE lea     rdi, [rsp+20h]
libc_2.23.so:00007FDFB90D26B3 call    near ptr unk_7FDFB90E4FD0
libc_2.23.so:00007FDFB90D26B8 test    eax, eax
libc_2.23.so:00007FDFB90D26BA jnz     short loc_7FDFB90D270E
libc_2.23.so:00007FDFB90D26BC mov     rax, fs:300h
libc_2.23.so:00007FDFB90D26C5 mov     [rsp+68h], rax
libc_2.23.so:00007FDFB90D26CA mov     rax, fs:2F8h
libc_2.23.so:00007FDFB90D26D3 mov     [rsp+70h], rax
libc_2.23.so:00007FDFB90D26D8 lea     rax, [rsp+20h]
libc_2.23.so:00007FDFB90D26DD mov     fs:300h, rax
libc_2.23.so:00007FDFB90D26E6 mov     rax, cs:off_7FDFB944CEB8
libc_2.23.so:00007FDFB90D26ED mov     rsi, [rsp+8]
libc_2.23.so:00007FDFB90D26F2 mov     edi, [rsp+14h]
libc_2.23.so:00007FDFB90D26F6 mov     rdx, [rax]
libc_2.23.so:00007FDFB90D26F9 mov     rax, [rsp+18h]
libc_2.23.so:00007FDFB90D26FE call    rax							 ; hello world 호출 부분
```
"Hello World!" 루틴을 호출하는 부분을 찾아보니 rax에 주소를 저장하고 rax를 call함으로써 호출이 되고있었다. 그렇지만 어떤 값에 의해서 rax가 바뀌는지는 찾지 못했다. 그래서 rax에 있는 값을 키를 입력받는 루틴의 주소인 0x400A03로 변조해봤고 올바른 루틴으로 강제로 흐름을 바꿨다.

```
LOAD:0000000000400A6B mov     edx, 80h                        ; nbytes
LOAD:0000000000400A70 mov     rsi, rax                        ; buf
LOAD:0000000000400A73 mov     edi, 0                          ; fd
LOAD:0000000000400A78 call    read
LOAD:0000000000400A7D cmp     rax, 9						  ; 패스워드가 8자리인지 확인
LOAD:0000000000400A81 jnz     short loc_400A92
LOAD:0000000000400A83 lea     rax, [rbp+s]
LOAD:0000000000400A8A mov     rdi, rax
LOAD:0000000000400A8D call    sub_40084E					  ; 패스워드가 맞는지 비교하는 루틴
LOAD:0000000000400A92
LOAD:0000000000400A92 loc_400A92:                             ; CODE XREF: password_f+7Ej
LOAD:0000000000400A92 mov     edx, cs:dword_6020C0
LOAD:0000000000400A98 mov     rax, cs:off_6020C8
LOAD:0000000000400A9F mov     esi, edx
LOAD:0000000000400AA1 mov     rdi, rax
LOAD:0000000000400AA4 call    sub_4007DD					  ; Keep Trying! 출력
```
이 프로그램은 무한 루틴이기 때문에 0041010에 bp를 걸고 에러 문구 다음 루틴을 통해서 시리얼 넘버를 판별하는 곳을 찾아본다. 확인 결과 00FA140B라는 곳으로 넘어오고 text영역임에도 불구하고 00FA13E7~0B까지는 이라는 Data double word가 존재했다. 
```
.text:00FA13E3 loc_FA13E3:                             ; CODE XREF: .text:00FA13DBj
.text:00FA13E3                                         ; .text:00FA13DDj
.text:00FA13E3 lea     eax, [ebp-20Ch]                 ; 입력한 값
.text:00FA13E9 push    eax
.text:00FA13EA call    loc_FA1560					   ; 시리얼 넘버와 입력한 값 비교
.text:00FA13EF add     esp, 4
.text:00FA13F2 movzx   ecx, al
.text:00FA13F5 test    ecx, ecx
.text:00FA13F7 jz      short loc_FA1406
.text:00FA13F9 lea     ecx, [ebp-20Ch]
.text:00FA13FF call    loc_FA1160
.text:00FA1404 jmp     short loc_FA140B
.text:00FA1406 ; ---------------------------------------------------------------------------
.text:00FA1406
.text:00FA1406 loc_FA1406:                             ; CODE XREF: .text:00FA13F7j
.text:00FA1406 call    sub_FA1010					   ; 틀렸다는 문구로 넘어가는 루틴
.text:00FA140B
.text:00FA140B loc_FA140B:                             ; CODE XREF: .text:00FA1404j
.text:00FA140B mov     eax, 1
.text:00FA1410 jmp     short loc_FA1436
--------------------------------------------------------------------------------------------
.text:00FA1010 sub_FA1010 proc near                    ; CODE XREF: .text:loc_FA1406p
.text:00FA1010 push    10h                             ; uType
.text:00FA1012 push    offset aError                   ; "Error!"
.text:00FA1017 push    offset Text                     ; "Invalid serial number. Try again! :-("
.text:00FA101C push    0                               ; hWnd
.text:00FA101E call    ds:MessageBoxW
.text:00FA1024 retn
.text:00FA1024 sub_FA1010 endp
```
data를 바꿔보니 어셈블리어 코드가 나왔고 시리얼 넘버가 틀렸을 때 나오는 루틴인 call sub_FA1010도 나왔다.
그 위에 call loc_FA1160로 가보면 Congratulations!라는 문구를 출력한다. 맞는 시리얼 넘버를 등록하면 이 루틴으로 가는 것 같다. 맞는 시리얼 넘버인지 검증하는 루틴을 찾는 중에 그 위로 보면 [ebp-20Ch]라는 곳에 입력한 값이 저장되있는 것을 알 수 있다.
loc_FA1560을 실행하고 나서 al의 값을 ecx에 저장해주고 ecx가 0인지 아닌지 판별한다. 따라서 al이 0이면 틀렸다는 문구로 넘어가는 루틴으로 가는 것이다. 임의의 값을 입력하고 동적으로 분석해본 결과 loc_FA1560을 동작하고 나면 al이 0이 되버려서 틀렸다는 문구로 넘어간다.
```
  if ( ((unsigned int)off_602088 ^ *(_BYTE *)a1) == 48 )
  {
    if ( (BYTE1((*off_602088)[0]) ^ *(_BYTE *)(a1 + 1)) == 120 )
    {
      if ( (BYTE2((*off_602088)[0]) ^ *(_BYTE *)(a1 + 2)) == 48 )
      {
        if ( (BYTE3((*off_602088)[0]) ^ *(_BYTE *)(a1 + 3)) == 48 )
        {
          if ( (BYTE4((*off_602088)[0]) ^ *(_BYTE *)(a1 + 4)) == 67 )
          {
            if ( (BYTE5((*off_602088)[0]) ^ *(_BYTE *)(a1 + 5)) == 84 )
            {
              if ( (BYTE6((*off_602088)[0]) ^ *(_BYTE *)(a1 + 6)) == 70 )
              {
                if ( (BYTE7((*off_602088)[0]) ^ *(_BYTE *)(a1 + 7)) == 123 )
                {
                  for ( i = 0; i < dword_602080; ++i )
                  {
                    buf = *(_BYTE *)((signed int)(((((unsigned int)((unsigned __int64)i >> 32) >> 29) + (_BYTE)i) & 7)
                                                - ((unsigned int)((unsigned __int64)i >> 32) >> 29))
                                   + a1) ^ *((_BYTE *)off_602088 + i);
                    write(1, &buf, 1uLL);
                  }
                  exit(1);
-------------------------------------------------------------------------------------
LOAD:0000000000602088 off_602088 dq offset qword_400C18
-------------------------------------------------------------------------------------
LOAD:0000000000400C18 qword_400C18 dq 5A12640444791601h
```
패스워드를 비교하는 루틴을 보니 위와 같았다. 입력한 패스워드와 off_602088을 xor 연산해서 값을 비교하고 있었다. 
```python
>>> print chr(0x30^0x1)+chr(0x78^0x16)+chr(0x30^0x79)+chr(0x30^0x44)+chr(0x43^0x4)+chr(0x54^0x64)+chr(0x46^0x12)+chr(0x7B^0x5A)
1nItG0T!
```
1nItG0T!를 입력하니 문제가 풀렸다.
```
Welcome to the Twinlight Zone!!!
Password: 1nItG0T!
0x00CTF{0bfU5c473D_PtR4Z3}

```
