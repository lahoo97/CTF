Replace
======================

## Description
```

```
## 분석 및 풀이
압축파일을 받아서 해제하면 Replace.exe 파일이 나온다. 프로그램을 실행해보면 입력받는 칸과 Check버튼이 있고 하단에 "Wrong"이라는 문구가 떠있다. 문구를 입력해보려고 하면 숫자외에 다른 문자는 들어가지 않는다. 아무 숫자를 입력하고 Check버튼을 누르면 비정상적으로 프로그램이 종료가 된다.
```
.text:0040104C push    esi
.text:0040104D mov     esi, [ebp+hDlg]
.text:00401050 push    0                               ; bSigned
.text:00401052 push    0                               ; lpTranslated
.text:00401054 push    3EAh                            ; nIDDlgItem
.text:00401059 push    esi                             ; hDlg
.text:0040105A call    ds:GetDlgItemInt
.text:00401060 mov     dword_4084D0, eax
.text:00401065 call    loc_40466F                      ; 핵심 부분
.text:0040106A xor     eax, eax
.text:0040106C jmp     loc_404690
.text:00401071 ; ---------------------------------------------------------------------------
.text:00401071
.text:00401071 loc_401071:                             ; CODE XREF: DialogFunc+36A4j
.text:00401071 jmp     short loc_401084
.text:00401073 ; ---------------------------------------------------------------------------
.text:00401073 push    offset String                   ; "Correct!"
.text:00401078 push    3E9h                            ; nIDDlgItem
.text:0040107D push    esi                             ; hDlg
.text:0040107E call    ds:SetDlgItemTextA
.text:00401084
.text:00401084 loc_401084:                             ; CODE XREF: DialogFunc:loc_401071j
.text:00401084 mov     eax, 1
.text:00401089 nop
.text:0040108A nop
```
분석을 해보면 start -> 기타 함수들 -> WinMain(x,x,x,x) -> DialogFunc 순으로 호출한다. Dialogfunc을 보면 "Correct!"라는 문구를 띄워주는 부분이 있지만 00401073으로 넘어가는 루틴이 없다. 아마 입력하는 숫자에 따라서 저 부분으로 보낼 수 있는 듯 하다. 일단 call sub_40466F부분에 브레이크를 걸고 123을 넣고 분석을 해봤다.
일단 입력한 값은 GetDlgItemInt함수를 통해서 eax에 7B(123)으로 저장이 된다. 그 후 dword_4084D0에 저장이 된 후 sub_40466F함수를 호출한다.
```
.text:0040466F sub_40466F proc near                    ; CODE XREF: DialogFunc+45p
.text:0040466F                                         ; DialogFunc+3689p ...
.text:0040466F call    loc_40467A
.text:0040466F ; ---------------------------------------------------------------------------
.text:00404674 dd 84D00581h
.text:00404678 db 40h, 0
.text:0040467A ; ---------------------------------------------------------------------------
.text:0040467A loc_40467A:                             ; CODE XREF: sub_40466Fj
.text:0040467A mov     dword_406016, 619060EBh
.text:0040467A ; END OF FUNCTION CHUNK FOR sub_40466F
.text:00404684 call    $+5
.text:00404689
.text:00404689 sub_404689 proc near                    ; CODE XREF: DialogFunc+367Ap
.text:00404689 inc     dword_4084D0                    ; 2번 증가
.text:0040468F retn
.text:0040468F sub_404689 endp
```
sub_40466F함수를 보면 위와 같다. 여기서 동작하는 것을 분석해보면 다음과 같다.
sub_40466F호출 -> loc_40467A호출 -> mov 동작 후에 call $+5(sub_404689) -> dword_4084D0 1증가 후 retn으로 call $+5 다음줄로 이동(inc dword_4084D0로 이동) -> dword_4084D0 1증가후 call loc_40467A 다음줄로 이동
```
.text:0040466F call    near ptr loc_404674+6
.text:0040466F sub_40466F endp ; sp-analysis failed
.text:0040466F
.text:00404674 ; ---------------------------------------------------------------------------
.text:00404674
.text:00404674 loc_404674:                             ; CODE XREF: sub_40466Fj
.text:00404674 add     dword_4084D0, 601605C7h
.text:0040467E inc     eax
.text:0040467F add     bl, ch
.text:00404681 pusha
.text:00404682 nop
.text:00404683 popa
.text:00404684 call    $+5
.text:00404689
.text:00404689 ; =============== S U B R O U T I N E =======================================
.text:00404689
.text:00404689
.text:00404689 sub_404689 proc near                    ; CODE XREF: DialogFunc+367Ap
.text:00404689 inc     dword_4084D0
.text:0040468F retn
.text:0040468F sub_404689 endp
```
즉, inc dword_404D0가 2번 동작한 후 call loc_40467A의 다음줄로 되돌아간다. eip가 0x404674를 가리키면서 0x40466F~0x404683까지의 코드가 변한다. 변한 코드를 보니 dword_4084D0에 0x601605C7을 증가시킨다. 그 후 똑같이 dword_404D0를 1씩 두번 증가시킨다. 그 후 DialogFunc으로 돌아온다.
```
.text:00404690
.text:00404690 loc_404690:                             ; CODE XREF: DialogFunc+4Cj
.text:00404690 mov     eax, dword_4084D0
.text:00404695 push    offset loc_40469F
.text:0040469A call    sub_404689                      ; inc     dword_4084D0
.text:0040469F
.text:0040469F loc_40469F:                             ; DATA XREF: DialogFunc+3675o
.text:0040469F mov     dword ptr ds:sub_40466F, 0C39000C6h
.text:004046A9 call    sub_40466F
.text:004046AE inc     eax
.text:004046AF call    sub_40466F
.text:004046B4 mov     dword ptr ds:sub_40466F, 6E8h
.text:004046BE pop     eax
.text:004046BF mov     eax, 0FFFFFFFFh
.text:004046C4 jmp     loc_401071
.text:004046C4 ; END OF FUNCTION CHUNK FOR DialogFunc
-------------------------------------------------------------------------------------------------
.text:0040466F loc_40466F:                             ; CODE XREF: DialogFunc+45p
.text:0040466F                                         ; DialogFunc+3689p ...
.text:0040466F mov     byte ptr [eax], 90h
.text:00404672 retn
```
DialogFunc으로 돌아와서 dword_4084D0의 값을 eax에 저장한다. 그 후 40466F주소의 바이너리를 C39000C6로 덮고 0x40466F를 호출한다. 보면 eax의 주소의 바이너리 1byte를 0x90으로 덮는다. 그 후 eax를 1증가시키고 0x40466F를 한번 더 호출한다. 그 후 DialogFunc의 loc_401071로 되돌아온다.
그렇지만 eax에 들어있는 값은 60160646로 60160646의 주소는 존재하지 않기에 에러문구가 나오면서 더 이상 동작하지 않는다. 60160646이라는 값은 "입력값(123) + 1 + 1 + 0x601605C7 + 1 + 1"이다. 즉 이를 이용해서 Correct라는 문구를 띄워야 한다.
```
.text:00401065 call    loc_40466F                      ; 핵심 부분
.text:0040106A xor     eax, eax
.text:0040106C jmp     loc_404690
.text:00401071 ; ---------------------------------------------------------------------------
.text:00401071
.text:00401071 loc_401071:                             ; CODE XREF: DialogFunc+36A4j
.text:00401071 jmp     short loc_401084
.text:00401073 ; ---------------------------------------------------------------------------
.text:00401073 push    offset String                   ; "Correct!"
.text:00401078 push    3E9h                            ; nIDDlgItem
.text:0040107D push    esi                             ; hDlg
.text:0040107E call    ds:SetDlgItemTextA
```
이 프로그램은 우리가 입력한 숫자에 따라 해당하는 주소의 바이너리를 0x90으로 덮는다. 0x90은 NOP으로 아무것도 실행하지 않고 넘어가는 명령어이다. 이 문제는 딱 2번 원하는 주소의 바이너리를 NOP으로 덮을 수가 있다. 0x401071을 호출하니까 0x401071부터 2byte를 nop으로 덮는다면 "Correct!"라는 문구가 뜰 것이다. 즉, 연산 결과가 0x401071이 되야 한다.
0x401071 - 1 - 1 - 0x601605C7 - 1 - 1 = FFFFFFFFA02A0AA6
즉, 0xA02A0AA6(2687109798)가 답이다.
답 : 2687109798