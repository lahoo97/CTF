Challenge-007
======================

-----------------
## Description
```

```

## 풀이
```
Program protected by HexaPass(TM)

Enter key: 
```
c4를 실행하면 다음과 같이 나온다. 그리고 아무값이나 넣어보면 "Wrong Key!"이라는 문구가 나온다.
```
__int64 sub_400856()
{
  __int64 result; // rax@3
  __int64 v1; // rcx@3
  char s[1032]; // [sp+10h] [bp-410h]@1
  __int64 v3; // [sp+418h] [bp-8h]@1

  v3 = *MK_FP(__FS__, 40LL);
  memset(s, 0, 0x400uLL);
  puts("Program protected by HexaPass(TM)\n");
  printf("Enter key: ", 0LL);
  fgets(s, 1024, stdin);
  s[(signed int)(strlen(s) - 1)] = 0;
  if ( (unsigned int)sub_4006FD((signed __int64)s) )
    puts("Wrong Key!\n");
  puts("--\nCrackme by pico\n  Greetings to the 0x00sec.org Community");
  result = 0LL;
  v1 = *MK_FP(__FS__, 40LL) ^ v3;
  return result;
}
```

ida로 분석을 해보면 fgets로 key를 입력받고 sub_4006FD에서 키를 확인한다. sub_4006FD가 key를 검증하는 루틴인것 같다.
```
signed __int64 __fastcall sub_4006FD(signed __int64 a1)
{
  char v2; // [sp+12h] [bp-Eh]@2
  char v3; // [sp+14h] [bp-Ch]@1
  signed __int64 v4; // [sp+18h] [bp-8h]@1
  signed __int64 v5; // [sp+18h] [bp-8h]@8

  v4 = a1;
  v3 = 0;
  while ( *(_BYTE *)v4 )
  {
    v2 = 0;													//첫번째 자리 비교
    if ( *(_BYTE *)v4 <= '/' || *(_BYTE *)v4 > '9' )		//0~9 숫자 판별
    {
      if ( *(_BYTE *)v4 > '`' && *(_BYTE *)v4 <= 'f' ) 		//a~f 소문자 알파벳 판별
        v2 = 16 * (*(_BYTE *)v4 - 87);
    }
    else
    {
      v2 = 16 * (*(_BYTE *)v4 - 48);						//결과값에 16진수로 왼쪽 시프트 연산
    }														//ex) 0xb -> 0xb0
    v5 = v4 + 1;											//두번째 자리 비교
    if ( !*(_BYTE *)v5 )
      return 0xFFFFFFFFLL;
    if ( *(_BYTE *)v5 <= '/' || *(_BYTE *)v5 > '9' )		//0~9 숫자 판별
    {
      if ( *(_BYTE *)v5 > '`' && *(_BYTE *)v5 <= 'f' )		//a~f 소문자 알파벳 판별
        v2 |= *(_BYTE *)v5 - 87;
    }
    else
    {
      v2 |= *(_BYTE *)v5 - 48;								//결과값과 v5 or연산
    }														//ex) ba입력시 : 0xb0 | 0x0a => 0xba
    if ( byte_601080[(unsigned __int64)(v3 & 3)] != v2 )	//2byte씩 비교
      return 1LL;
    ++v3;
    v4 = v5 + 1;
  }
}
```
while문은 크게 두자리를 비교하고 있다. 키값은 공통적으로 0~9와 a~f로 이루어져야 한다. 첫번째 자리 비교에서는 0~9, a~f를 만족하면 왼쪽으로 시프트 연산을 해준다.(0xb -> 0xb0) 그리고 두번째 자리 비교에서는 0~9, a~f를 만족하면 첫번째 자리 결과값과 두번째 자리값을 or연산을 해준다. (ba입력 : 0xb0 | 0x0a = 0xba) 그 후 byte_601080과 2bte씩 비교를 하고있다. byte_601080을 보면 babecab1가 저장되어있다. 따라서 babecab1을 키로 입력해주면 문제가 풀린다.

```
./c4
Program protected by HexaPass(TM)

Enter key: babecab1
**********************
**  0x00CTF{H3x4p4sS_SucK5!-babecab1-R0cK5!}
**********************
Greetings to:
                                                                                
  .:xKOo'              ,dKKd;.   'd0Kx:.   :ddddddddd: 'dddddddd:   :dddddddd;  
 kMMMMMMMN.          'NMMMMMMWo.NMMMMMMWd  OMMMMMMMMMO lMMMMMMMM0 :NMMMMMMMMMk  
 0MW00MMMM'          ,MMXkXMMMk.MMNkOMMMk  OMMMx''KMMO lMMMK''''. OMMMx''xMMMk  
 d:. lMMMW...      . 'x'  OMMMx.O'  lMMMk  OMMMK:..''. lMMM0....  OMMMl  :XXXd  
 ONO:dMMMM'kWOc.'lOW',WOl'OMMMk'W0o,dMMMk  .dKMMMWO;   lMMMMMMMMl OMMMl         
 0MMMo'lON'kMMMMMMX: ,MMMM;:xNk'MMMMd;dXk     'dNMMMNc lMMMNdddd' OMMMl         
 0MMMl .:O..lNMMMMMW.,MMMM' ,xd.WMMMl 'dd  ,:::. dMMMO lMMMO      OMMMl  .:::'  
 0MMMKKMMM':KW0dxKMM',MMMM0NMMk'MMMMXNMMk  OMMMO:xMMMO lMMMX::::: OMMMO::OMMMk  
 dWMMMMMM0.;:.    .c..XMMMMMMX:.0MMMMMMNo  OMMMMMMMMMO lMMMMMMMMM.OMMMMMMMMWx.  
   'dOx:.              'lkOo'    .ckOd'    ,:::::::::, .::::::::: ,::::::::.    
                                                                                
--
Crackme by pico
  Greetings to the 0x00sec.org Community
```
