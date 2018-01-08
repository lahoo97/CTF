Challenge-001
======================

-----------------
## Description
```

```

## 풀이
```
Serial Number:
_____________________  register
```
Challenge-001.exe를 실행하면 다음과 같이 나온다.
아무 값이나 입력 후 register을 누르면 "Invalid serial number. Try again! :-("라는 문장이 나온다.
```
.text:00FA1010                 push    10h             ; uType
.text:00FA1012                 push    offset aError   ; "Error!"
.text:00FA1017                 push    offset Text     ; "Invalid serial number. Try again! :-("
.text:00FA101C                 push    0               ; hWnd
.text:00FA101E                 call    ds:MessageBoxW
.text:00FA1024                 retn
.text:00FA1024 sub_FA1010      endp
```
Ida로 확인 결과 Invalid serial number. Try again! :-(를 출력하는 부분을 찾았다. 그러나 이 부분으로 오는 곳은 찾지 못했다. 그러나 분명히 에러 문구는 출력이 되었으므로 이 부분으로 오는 루틴이 숨겨져 있는 것 같다.
```
.text:00FA13E7 byte_FA13E7 db 0FFh                     ; CODE XREF: .text:00FA13DDj
.text:00FA13E8 dd 71E850FFh, 83000001h, 0B60F04C4h, 74C985C8h, 0F48D8D0Dh, 0E8FFFFFDh
.text:00FA13E8 dd 0FFFFFD5Ch, 5E805EBh
.text:00FA1408 db 0FCh, 0FFh, 0FFh
.text:00FA140B ; ---------------------------------------------------------------------------
.text:00FA140B mov     eax, 1					<----------------------- EIP
.text:00FA1410 jmp     short loc_FA1436
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
.text:00FA1587 loc_FA1587:                             ; CODE XREF: .text:00FA157Ej
.text:00FA1587 call    sub_FA1490
.text:00FA158C cmp     eax, 0Dh                        ; 13자리 이상인지 판별
.text:00FA158F jnb     short loc_FA1595
.text:00FA1591 xor     al, al
.text:00FA1593 jmp     short loc_FA15F3
```
loc_FA1560루틴을 쭉 찾아 내려가는 도중 시리얼 넘버의 자리수가 13자리 이상인지 체크하는 부분을 확인했다. 
```
.text:00FA15CA loc_FA15CA:                             ; CODE XREF: .text:00FA15C1j
.text:00FA15CA call    sub_FA1030
.text:00FA15CF mov     edx, [ebp-8]                    ; 맞는 시리얼 넘버
.text:00FA15D2 mov     ecx, [ebp+8]                    ; 입력한 값
.text:00FA15D5 call    sub_FA1450                      ; 시리얼 넘버와 입력값 비교
-------------------------------------------------------------------------------------
.text:00FA1450 mov     ax, [ecx]
.text:00FA1453 cmp     ax, [edx]
.text:00FA1456 jnz     short loc_FA147A
.text:00FA1458 test    ax, ax
.text:00FA145B jz      short loc_FA1472
.text:00FA145D mov     ax, [ecx+2]
.text:00FA1461 cmp     ax, [edx+2]
.text:00FA1465 jnz     short loc_FA147A
.text:00FA1467 add     ecx, 4
.text:00FA146A add     edx, 4
.text:00FA146D test    ax, ax
.text:00FA1470 jnz     short sub_FA1450

```
그 밑으로 내려가보니 ecx에 입력한 값이 저장되있는 것을 확인했고 edx에는 "0G932SE1L48Y6G"라는 값이 저장되어 있었다. sub_FA1450으로 들어가보니 ecx와 edx에 있는 값을 두자리씩 비교를 하고 있었다. edx에 있는 값은 맞는 시리얼 넘버로 추측이 된다.
"0G932SE1L48Y6G"을 입력했더니 키값이 나왔다.
```
0x00CTF{F1SH1N9_R3QU1R3S_G00D_B4IT}
```
