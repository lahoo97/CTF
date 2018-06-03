Direct3D_FPS
======================

## Description
```

```
## 분석 및 풀이
FPS.exe를 시랭해보면 총게임이 실행이 된다. 게임을 조금 해보면 이상하게 생긴 적들이 움직이고 있고 총으로 계속 쏘다보면 사라진다. 적을 다 죽여도 게임이 끝나지는 않지만 적에게 닿으면 hp가 0이 되고 "Game Over! You are dead"라는 문구가 뜨면서 프로그램이 끝난다.
<a id="[그림1]">[그림1]</a>
```
.text:013E39C0 sub_13E39C0 proc near                   ; CODE XREF: WinMain(x,x,x,x):loc_13E2F4C
.text:013E39C0 mov     eax, offset dword_13E9194
.text:013E39C5
.text:013E39C5 loc_13E39C5:                            ; CODE XREF: sub_13E39C0+14j
.text:013E39C5 cmp     dword ptr [eax], 1
.text:013E39C8 jz      short locret_13E3A01
.text:013E39CA add     eax, 210h
.text:013E39CF cmp     eax, offset unk_13EF8B4
.text:013E39D4 jl      short loc_13E39C5
.text:013E39D6 mov     eax, hWnd
.text:013E39DB push    40h                             ; uType
.text:013E39DD push    offset aGameClear               ; "Game Clear!"
.text:013E39E2 push    offset byte_13E7028             ; lpText
.text:013E39E7 push    eax                             ; hWnd
.text:013E39E8 call    ds:MessageBoxA
.text:013E39EE mov     ecx, hWnd
.text:013E39F4 push    0                               ; lParam
.text:013E39F6 push    0                               ; wParam
.text:013E39F8 push    2                               ; Msg
.text:013E39FA push    ecx                             ; hWnd
.text:013E39FB call    ds:SendMessageA
.text:013E3A01
.text:013E3A01 locret_13E3A01:                         ; CODE XREF: sub_13E39C0+8j
.text:013E3A01 retn
```
게임오버 문구를 검색해보면 게임오버 루틴을 찾을 수 있다. 체력이 0보다 크면 loc_13E2F4C으로 프로그램이 도는데 바로 거기에 있는 sub_13E39C0함수를 보면 위와 같이 Game Clear!"라는 문구를 보게 되있다. 일단 MessageBox로 출력되는 문구가 궁금해서 강제로 메세지를 띄웠으나 이상한 문구가 떴다. 이 문제는 메시지가 암호화되 있는듯 했다.
"Game Clear!"로 가려면 dword_13E9194 + (0x210 * i)의 값이 1이 아니어야 한다. 
```
[그림2]
.text:013E3400 sub_13E3400 proc near                   ; CODE XREF: WinMain(x,x,x,x)+750p
.text:013E3400 push    ecx
.text:013E3401 call    sub_13E3440
.text:013E3406 cmp     eax, 0FFFFFFFFh
.text:013E3409 jz      short loc_13E343E
.text:013E340B mov     ecx, eax
.text:013E340D imul    ecx, 210h
.text:013E3413 mov     edx, dword_13E9190[ecx]
.text:013E3419 test    edx, edx
.text:013E341B jg      short loc_13E3435
.text:013E341D mov     dword_13E9194[ecx], 0           ; dword_13E9194에 관여하는 부분
.text:013E3427 mov     cl, byte_13E9184[ecx]
.text:013E342D xor     byte_13E7028[eax], cl           ; 핵심부분
.text:013E3433 pop     ecx
.text:013E3434 retn
.text:013E3435 ; ---------------------------------------------------------------------------
.text:013E3435
.text:013E3435 loc_13E3435:                            ; CODE XREF: sub_13E3400+1Bj
.text:013E3435 add     edx, 0FFFFFFFEh
.text:013E3438 mov     dword_13E9190[ecx], edx
.text:013E343E
.text:013E343E loc_13E343E:                            ; CODE XREF: sub_13E3400+9j
.text:013E343E pop     ecx
.text:013E343F retn
```
dword_13E9194에 관여하는 부분을 찾아보면 해당 함수가 검색이 되었다. 해당 함수에 브레이크를 걸거 동적으로 분석해봤다. 적을 맞추면 해당 함수에 브레이크가 걸렸다. eax값을 보면 적마다 고유 번호(0x00~0x30)를 갖고 있었고 체력은 0x64(100)로 동일했다. 적을 맞추면 dword_13E9190[ecx]에 있는 숫자가 점점 감소하고 0이 되는 순간 dword_13E9194에 관여하는 부분으로 넘어간다. 실제로 0x00의 고유번호를 갖는 적을 죽이고 나니 .text:013E39C5에서의 루틴이 한바퀴 돌았다.
이때  byte_13E7028와 cl이 xor 연산을 한번 하게 된다. byte_13E7028는 [[그림1]](#[그림1])에 "Game Clear!" 문구와 함께 나오는 깨진 문자열이였다. 적을 죽이면 byte_13E7028와 0x4의 배수(0부터)와 xor연산을 하게 된다.

```python
str1 = "43 6B 66 6B 62 75 6C 69 4C 45 5C 45 5F 5A 46 1C 07 25 25 29 70 17 34 39  01 16 49 4C 20 15 0B 0F F7 EB FA E8 B0 FD EB BC F4 CC DA 9F F5 F0 E8 CE F0 A9"
result = ""
str1 = str1.replace(" ","")
for i in range(0x00, len(str1),2):
    result += chr((int(("0x"+str1[i:i+2]),0)) ^ (i*4/2))

print result
# python exploit.py
Congratulation~ Game Clear! Password is Thr3EDPr0m
```
정답 : Thr3EDPr0m