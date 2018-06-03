Easy_Unpack
======================

## Description
```
//ReadMe.txt
ReversingKr UnpackMe


Find the OEP

ex) 00401000
```
## 분석 및 풀이
압축파일을 받아서 해제하면 Easy_UnpackMe.exe와 ReadMe.txt라는 파일이 나온다. ReadMe.txt를 보면 OEP를 찾으라고 나온다. Packing이 되있으면 바이너리가 비정상적이고 프로그램의 시작위치 등도 알 수 없게 되있다. Packing된 프로그램을 실행시 자동으로 Unpacking이 된 후 원래의 코드가 실행이 되게 된다. 이때 Unpacking이 되있던 원래의 코드가 정상적으로 실행이 되려면 원본 코드의 시작 지점에서부터 실행이 되어야 하는데 이 시작 지점은 OEP(Original Entry Point)라고 한다. 결국 Unpacking이 끝나고 나면 OEP로 점프를 시켜야 되므로 Unpacking이 끝나는 부분을 찾아볼 것이다.
```
.GWan:0040A08F mov     ecx, offset loc_409000          ; 시작 주소
.GWan:0040A094 mov     edx, offset loc_4094EE          ; 끝나는 주소
.GWan:0040A099
.GWan:0040A099 loc_40A099:                             ; CODE XREF: start+76j
.GWan:0040A099 cmp     ecx, edx
.GWan:0040A09B jz      short loc_40A0C3
.GWan:0040A09D xor     byte ptr [ecx], 10h             ; 
.GWan:0040A0A0 inc     ecx
.GWan:0040A0A1 cmp     ecx, edx
.GWan:0040A0A3 jz      short loc_40A0C3
.GWan:0040A0A5 xor     byte ptr [ecx], 20h
.GWan:0040A0A8 inc     ecx
.GWan:0040A0A9 cmp     ecx, edx
.GWan:0040A0AB jz      short loc_40A0C3
.GWan:0040A0AD xor     byte ptr [ecx], 30h
.GWan:0040A0B0 inc     ecx
.GWan:0040A0B1 cmp     ecx, edx
.GWan:0040A0B3 jz      short loc_40A0C3
.GWan:0040A0B5 xor     byte ptr [ecx], 40h             
.GWan:0040A0B8 inc     ecx
.GWan:0040A0B9 cmp     ecx, edx
.GWan:0040A0BB jz      short loc_40A0C3
.GWan:0040A0BD xor     byte ptr [ecx], 50h
.GWan:0040A0C0 inc     ecx
.GWan:0040A0C1 jmp     short loc_40A099
```
 제일 처음 부분을 보면 분기점이 여러개로 나뉘어 있다. ecx에 시작되는 주소를 저장하고 edx에 기준이 되는 주소를 저장한다. 그 후 ecx와 edx가 같아질때까지 연산을 하는데 ecx에 있는 주소의 바이너리 1byte와 10h, 20h, 30h, 40h, 50h를 차례대로 xor연산을 시킨다. 그렇게 되면 409000~4094EE까지 바이너리가 원상태로 돌아오게 된다.

 아래를 계속 분석해보면 전부 같은 패턴이다. 409000~4049EE, 401000~405000, 406000~409000주소에 대해서 각각 같은 방식으로 연산을 시킨 후 loc_401150으로 점프를 시킨다.
```
.text:00401150
.text:00401150 loc_401150:
.text:00401150 push    ebp
.text:00401151 mov     ebp, esp
.text:00401153 push    0FFFFFFFFh
.text:00401155 push    offset unk_4050D0
.text:0040115A push    offset dword_401E1C
.text:0040115F mov     eax, large fs:0
.text:00401165 push    eax
.text:00401166 mov     large fs:0, esp
.text:0040116D sub     esp, 58h
.text:00401170 push    ebx
.text:00401171 push    esi
.text:00401172 push    edi
.text:00401173 mov     [ebp-18h], esp
.text:00401176 call    ds:off_40503C
.text:0040117C xor     edx, edx
```
loc_401150으로 점프한 후를 보면 전형적인 프롤로그가 나온다. 조금더 분석을 해보면 역시나 이 부분이 원래 동작하는 코드의 OEP임을 알 수 있다.

정답 : 00401150