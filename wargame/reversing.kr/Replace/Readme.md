Music_Player
======================

-----------------
## Description
```
//ReadMe.txt
This MP3 Player is limited to 1 minutes.
You have to play more than one minute.

There are exist several 1-minute-check-routine.
After bypassing every check routine, you will see the perfect flag.

```
## 분석 및 풀이
Music_Player.exe를 실행후 아무 음악파일을 넣고 실행해봤다. 1분이 다 되면 "1분 미리듣기만 가능합니다."라는 문구가 뜬다. 어디엔가 1분을 검증하는 부분이 있을 것이다. 
```
.text:0040455D mov     eax, [ebp+var_A4]
.text:00404563 cmp     eax, 60000      ; 1분 검증 루틴
.text:00404568 mov     [ebp+var_18], eax
.text:0040456B jl      loc_4045FE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.text:004045C6 lea     edx, [ebp+var_60]
.text:004045C9 lea     eax, [ebp+var_50]
.text:004045CC push    edx
.text:004045CD lea     ecx, [ebp+var_40]
.text:004045D0 push    eax
.text:004045D1 push    ecx
.text:004045D2 lea     edx, [ebp+var_30]
.text:004045D5 push    40h
.text:004045D7 push    edx
.text:004045D8 call    ds:rtcMsgBox
```
1분은 검증하는 루틴을 알기 위해서 vba 함수에 대해서 검색을 해봤다. vba 함수에서는 1000이 1초를 나타내기때문에 1분이면 60000(EA60)과 비교하는 구문이 있을 것이다. 검색해보니 딱 한 부분만이 존재햇다. 이 부분에 브레이크를 걸고 동적으로 분석해봤다. 동적으로 분석할때 파일을 찾기 위해서 Open을 하게 되면 에러나 나는데 정확한 원인을 잘 모르겠다. 현재로써는 Open으로 여는 대신 직접 파일의 경로를 적어주면 에러가 나는 것을 우회할 수 있다. 
동적으로 분석시 매 일정 시간마다 sub_4044C0안에 있는 저 검증 루틴으로 1분이 초과했는지 확인하고 있다. 일정 시간 뒤에 분석을 하면 loc_4045FE로 넘어가지 않고 다른 방향으로 동작하게 된다. 그 후 rtcMsgBox와 만나서 "1분 미리듣기만 가능합니다."라는 문구가 나온다. 60초를 초과했을때 loc_4045FE로 넘어가지 않기 때문에 SF레지스터가 세트(1)되있는 것을 해제(0)해서 강제로 loc_4045FE 보내고 실행을 하니 메모리 생겼다. 아마 다른 방식으로 검증하는 부분이 있는 듯 하다. 
```
.text:004046A7 test    eax, eax
.text:004046A9 fnclex
.text:004046AB jge     short loc_4046BF
.text:004046AD push    0BCh
.text:004046B2 push    offset dword_402B58
.text:004046B7 push    edi
.text:004046B8 push    eax
.text:004046B9 call    ds:__vbaHresultCheckObj
.text:004046BF
.text:004046BF loc_4046BF:                             ; CODE XREF: sub_4044C0+1EBj
.text:004046BF lea     ecx, [ebp+var_20]
.text:004046C2 call    ds:__vbaFreeObj
.text:004046C8 xor     ebx, ebx
```
loc_4045FE이후로 계속 보면 원래 60초가 넘기 전과 넘은 후가 다르게 동작하는 부분을 찾았다. 60초가 넘기 전에는 조건이 충족하여 loc_4046BF로 넘어갔었는데 60초가 넘은 후에는 loc_4046BF로 넘어가지 않았다. 혹시나해서 F7로 vbaHresultCheckObj함수로 넘어가서 동작을 보니 얼마 안가서 아까와 같은 에러가 나왔다. 따라서 vbaHresultCheckObj로 넘어가면 안된다는 것을 파악했다. 저 부분을 넘어가니 1분이 넘었는데도 음악이 계속 실행이 되고 있고 "MP3 Player"라는 타이틀이 사라지고 패스워드가 나왔다.
Password is LIstenCare
