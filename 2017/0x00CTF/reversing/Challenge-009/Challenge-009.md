Challenge-009
======================

-----------------
## Description
```

```

## 풀이
```
$./sc04
--------------------------------------------
Guess the password and save the day
=> Password :
```
sc04를 실행하면 다음과 같이 나온다. 그리고 아무값이나 넣어보면 "0x00CTF{oops!...Keep trying!}"이라는 문구가 나온다. 그렇지만 해당 문구를 출력하는 offset은 어디에도 존재하지 않았다. 대신 알 수 없는 offset이 있는 것으로 봐서 문구들은 모두 암호화되있는듯 하다.
```
void __fastcall __noreturn sub_400CD6(const char *a1)
{
  signed int v1; // [sp+1Ch] [bp-4h]@2

  decrypt_print_40077D(4199011LL, 8u);
  if ( strlen(a1) > 7 )		; 입력한 패스워드 길이는 7이상이다.
  {
    v1 = 0;
    while ( ((unsigned __int8)byte_401288[(signed __int64)v1] ^ a1[v1]) == (unsigned __int8)byte_4012B0[(signed __int64)v1] )
    {
      putchar(a1[v1] ^ (unsigned __int8)byte_4012D8[(signed __int64)v1]);
      ++v1;
      if ( v1 > 33 )			; 패스워드는 34자리이다.
      {
        puts("}");
        exit(1);
      }
    }
  }
  decrypt_print_40077D(4199023LL, 0x16u);
  exit(1);
}
```
분석을 해보면 fgets로 password를 입력받고 sub_400CD6에서 패스워드를 확인한다. 입력한 패스워드 길이가 7이상이 되야 루프를 돌면서 비교를 시작하고 총 34자리를 비교한 뒤 종료한다. 루프에서는 byte_401288와 입력한 패스워드와 xor연산을 한 값과 byte_4012B0값이 같으면 입력한 패스워드와 byte_4012D8을 xor연산해서 출력해준다.
```
byte_401288 = "F4 B4 4A 3F F2 01 B7 4E 81 F6 5F 21 3D CB E7 BF D8 2A 31 BA 40 ED 39 82 A8 76 31 5E 02 3F F7 FC 70".split()
s1 = ("".join(byte_401288))+"00"
#print s1

byte_4012B0 = "A7 DD 3E 4B 9B 6F D8 20 D5 9E 3A 65 52 A8 8C F0 BE 7E 59 DF 02 8C 40 D5 C9 05 45 37 6C 58 A3 95 1D 65".split()
s2 = "".join(byte_4012B0)
#print s2

result = int(s1,16) ^ int(s2,16)
print hex(result)[2:70].decode("hex")
#SittinonTheDockOfTheBayWastingTime
0x00CTF{Th1s_i5_n07_th3_fl4G_Y0uR_l0Ok1n_4}
```
두 offset을 xor 연산하면 원하는 입력값을 알 수 있었지만 입력한 결과 플래그가 아니라는 문구가 출력이 된다. main함수와 key를 체크하는 함수 외에도 많은 함수가 존재하므로 나머지 함수들도 분석을 해봤다.
```
int sub_400A1C()
{
  signed int i; // [sp+0h] [bp-20h]@1
  signed int v2; // [sp+0h] [bp-20h]@7

  for ( i = 0; i < 2914 && dword_60218C <= 8; ++i )
  {
    if ( *((_BYTE *)qword_400000 + i) == -61 )
      *(&qword_6021A0 + dword_60218C++) = (int (*)(void))(i + 0x400000LL);
  }
  v2 = -1;
  while ( 1 )
  {
    ++v2;
    if ( !environ[v2] )
      return qword_6021A8();
    if ( !environ[v2] || strlen(environ[v2]) != 10 )
      break;
    if ( *environ[v2] == 77     ; M
      && environ[v2][1] == 65   ; A 
      && environ[v2][2] == 73   ; I
      && environ[v2][3] == 78   ; N
      && environ[v2][4] == 61   ; =
      && environ[v2][5] == 51   ; 3
      && environ[v2][6] == 49   ; 1
      && environ[v2][7] == 49   ; 1
      && environ[v2][8] == 55   ; 7
      && environ[v2][9] == 51 ) ; 3
      return qword_6021A0();
  }
  return qword_6021B0();
}
----------------------------------------------------------------
00007FFFE30CACB8 dq offset aLs_colorsRs0Di0132L          ; "LS_COLORS=...
00007FFFE30CACC0 dq offset aVirtualenvwrapper_h          ; "VIRTUALENV...
00007FFFE30CACC8 dq offset aLangEn_us_utf8               ; "LANG=en_U...
00007FFFE30CACD0 dq offset a_virtualenvwrapper_          ; "_VIRTUALENVWR...
00007FFFE30CACD8 dq offset aWorkon_homeRoot_env          ; "WORKON_HOM...
00007FFFE30CACE0 dq offset aS_colorsAuto                 ; "S_COLOR...
00007FFFE30CACE8 dq offset aUserRoot                     ; "USE...
00007FFFE30CACF0 dq offset aPwdRootDesktop               ; "PWD...
00007FFFE30CACF8 dq offset aHomeRoot                     ; "HOME...
00007FFFE30CAD00 dq offset aMailVarMailRoot              ; "MAI...
00007FFFE30CAD08 dq offset aVirtualenvwrapper_s          ; "VIRTUALENVWR..
00007FFFE30CAD10 dq offset aShellBinBash                 ; "SHELL...
00007FFFE30CAD18 dq offset aTermXterm                    ; "TERM=...
00007FFFE30CAD20 dq offset aShlvl1                       ; "SHLVL...
00007FFFE30CAD28 dq offset aLognameRoot                  ; "LOGNAME...
.....
```
함수들 중에 sub_400A1C라는 함수를 보니 환경변수를 가져와서 "MAIN=31173"이라는 문구와 비교해주는 부분이 있었다. 실제로 스택을 확인해보니 환경변수들을 불러오고 있었다. 환경변수들중에서 제일 처음 offset의 값과 "MAIN=31173"을 비교해주고 있었다. 프로그램이 실행이 될때 "MAIN=31173"이라는 환경변수가 제일 위에 있으면 될 것이다. MAIN=31173을 환경변수에 추가해줄때 주의사항은 환경변수다보니 분석환경의 터미널에서 추가해주지 않으면 의미가 없어진다.
```
$ MAIN=31173 ./sc04
Congrats!. You have found the real challenge!!! Let's Play
Password :
```
환경변수를 맞춰준 상태에서 실행하니까 새로운 문구가 나왔고 이 루틴이 맞는 루틴인듯 하다. sc04를 실행해두고 attach를 해서 분석했다.
```
0000000000402115 db  55h ; U                             ; DATA XREF: sub_4007DC+2Fo
0000000000402116 db  48h ; H
0000000000402117 db  89h ; 
0000000000402118 dq 0A0EC8148E5h, 8948FFFFFF6CBD89h, 8B4864FFFFFF60B5h, 8948000000282504h
0000000000402118 dq 3BBEC031F845h, 32E800401380BF00h, 0BBEFFFFE6h, 0E623E8004013BCBFh, 1FFFFF158B48FFFFh
0000000000402118 dq 0FFFFFF70858D4800h, 0C7894800000080BEh
0000000000402170 ; ---------------------------------------------------------------------------
0000000000402170 call    fgets
0000000000402175 lea     rax, [rbp-90h]
000000000040217C mov     rdi, rax
000000000040217F call    sub_402000
0000000000402184 mov     eax, 0
0000000000402189 mov     rcx, [rbp-8]
000000000040218D xor     rcx, fs:28h
0000000000402196 jz      short locret_40219D
0000000000402198 call    _stack_chk_fail
```

F8을 눌러서 계속 실행해보면 RIP관련된 메세지박스가 뜬다. 이 메세지박스는 보통 코드가 있지만 코드를 undefined시켜놔서 RIP가 가리키고 있을수 없을때 봤다. 예를 누르면 위와같이 갑자기 fgets함수를 call하는 코드가 생긴다. 코드 패치를 마저 진행시키면 0x402115~0x40219E까지 하나의 함수인 것을 알 수있다. 아까 거짓된 루틴에서와 같이 이 함수에서도 fgets로 Password를 입력받고 sub_402000이라는 함수를 호출한다. 이 프로그램의 핵심은 sub_402000인듯 하다.
```
signed __int64 __fastcall sub_402000(const char *a1)
{
  int v1; // eax@2
  int i; // [sp+14h] [bp-Ch]@4
  signed int j; // [sp+14h] [bp-Ch]@8
  int v5; // [sp+18h] [bp-8h]@1
  int v6; // [sp+1Ch] [bp-4h]@4

  v5 = 0;
  if ( strlen(a1) > dword_6020A0 )	; dword_6020A0 = 0x12
    v1 = dword_6020A0;
  else
    v1 = strlen(a1);
  v6 = v1;
  for ( i = 0; i < v6; ++i )
    v5 += ((int (__fastcall *)(_QWORD, const char *, _QWORD))*(&off_6020C0 + i))(a1[i], a1, (unsigned int)i);		; offset에 있는 주소에 해당하는 함수를 호출한다.
  if ( v5 )
  {
    decrypt_print_40077D(4198925LL, 6u);
  }
  else
  {
    for ( j = 0; j < dword_602080; ++j )
      putchar((char)(off_602078[j] ^ a1[j % 18]));
  }
  putchar(10);
  return 1LL;
}
```
sub_402000를 보면 첫 if문에서 처음에 입력한 Password길이가 0x12(18)인지 체크를 하고 있다. 18자리의 아무값이나 입력을 하면 if(v5)루틴으로 가면서 "Oops!"라는 문구와 함께 종료가 되므로 v5를 0으로 만들어서 else로 빠지게 해야한다. v5는 바로 위의 for문에서 연산이 되고있다. for문에서는 [offset+i]에 저장 되어있는 함수를 호출하고 반환값을 v5에 저장하고 있다. i값이 증가하므로 매번 다른 함수값을 호출할 것이고 이는 0x12(18)번 호출이 될 것이다.
```
00000000006020C0 off_6020C0 dq offset sub_40219F
00000000006020C8 dq offset sub_4024D5
00000000006020D0 dq offset sub_40278F
00000000006020D8 dq offset sub_402AC5
00000000006020E0 dq offset sub_402DAF
00000000006020E8 dq offset sub_40309C
00000000006020F0 dq offset sub_40337D
00000000006020F8 dq offset sub_403656
0000000000602100 dq offset sub_40390C
0000000000602108 dq offset sub_403C67
0000000000602110 dq offset sub_403F8B
0000000000602118 dq offset sub_40421B
0000000000602120 dq offset sub_4044D7
0000000000602128 dq offset sub_4047CB
0000000000602130 dq offset sub_404AB5
0000000000602138 dq offset sub_404DBE
0000000000602140 dq offset sub_4050AE
0000000000602148 dq offset sub_4053A5
```
sub_40219F 함수 이후로 호출될 함수들이 저장되어있는 것도 확인했다. 
```
_int64 __fastcall sub_40219F(char a1, __int64 a2, int a3)
{
  int v3; // ST4C_4@1
  int v4; // ST48_4@1
  int v5; // ST44_4@1
...
...
  return v12 ^ v12 ^ a1 ^ 0x70u;
}
```
제일 처음 함수를 보면 "v12 ^ v12 ^ a1 ^ 0x70"을 반환하고 있다. 여기서 a1은 입력한 Password값이다.
v12 ^ v12의 값은 0이고 0 ^ a1 = a1이다. 반환값을 0으로 만들기 위해서는 입력한 값이 0x70이면 되었고 함수 자체는 수많은 연산을 하고 있지만 아무의미가 없었다. 나머지 함수들도 형태는 조금씩 다르지만 return 값은 특정값과 입력한 값이 일치하면 되었다.
```
$ MAIN=31173 ./sc04
Congrats!. You have found the real challenge!!! Let's Play
Password : p1C0bfU5K4t0R-2o1T
0x00CTF{1tw4SaL0nGtR1p}
```