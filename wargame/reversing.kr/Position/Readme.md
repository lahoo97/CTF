Position
======================

## Description
```
//ReadMe.txt
ReversingKr KeygenMe


Find the Name when the Serial is 76876-77776
This problem has several answers.

Password is ***p
```
## 분석 및 풀이
ReadMe.txt를 보면 76876-77776에 해당하는 이름을 찾으라고 나온다. Position.exe를 실행해보면 name과 Serial을 입력하는 칸이 있고 아래에는 "Wrong"이라는 문구가 있다.
```
int __thiscall sub_2B1CD0(int this)
{
  int v1; // esi@1
  signed int v2; // eax@1
  int v3; // ecx@1
  int result; // eax@2

  v1 = this;
  v2 = sub_2B1740(this);
  v3 = v1 + 188;
  if ( v2 )
    result = CWnd::SetWindowTextW(v3, L"Correct!");
  else
    result = CWnd::SetWindowTextW(v3, L"Wrong");
  return result;
}
```
프로그램상에 Wrong이라는 문구가 있기 때문에 문구를 기반으로 검색해보면 위와 같은 코드가 나온다. sub_2B1740 함수의 결과에 따라서 분기가 결정이 된다.
```
 if ( *(_DWORD *)(name - 12) == 4 ) //4글자인지 검증
  {
    v4 = 0;
    while ( (unsigned __int16)ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, v4) >= 'a'
         && (unsigned __int16)ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, v4) <= 'z' )
```
sub_2B1740함수 내부로 들어가니 수많은 검증이 있었다. 첫번째로 name의 조건은 4글자여야 한다. 그렇지만 ReadMe.txt에서 힌트로 4글자인것은 이미 알고 있다. 두번째 name의 조건은 소문자 a~z만 사용해야 되는 것이다. GetAt함수로 입력된 name을 한글자씩 소문자가 만족하는지 검증하고 있었다.
```
 while ( 1 )
        {
          if ( v1 != v5 )
          {
            v6 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, v5);
            if ( (unsigned __int16)ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, v1) == v6 )
              goto LABEL_2;
          }
          ++v5;
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        }
```
세번째 조건으로는 name의 알파벳은 겹치면 안된다는 것이다. 이 이후부터는 연산을 통해서 총 10차례 검증을 했다.
```

```
DialogFunc으로 돌아와서 dword_4084D0의 값을 eax에 저장한다. 그 후 40466F주소의 바이너리를 C39000C6로 덮고 0x40466F를 호출한다. 보면 eax의 주소의 바이너리 1byte를 0x90으로 덮는다. 그 후 eax를 1증가시키고 0x40466F를 한번 더 호출한다. 그 후 DialogFunc의 loc_401071로 되돌아온다.
그렇지만 eax에 들어있는 값은 60160646로 60160646의 주소는 존재하지 않기에 에러문구가 나오면서 더 이상 동작하지 않는다. 60160646이라는 값은 "입력값(123) + 1 + 1 + 0x601605C7 + 1 + 1"이다. 즉 이를 이용해서 Correct라는 문구를 띄워야 한다.
```
v7 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, 0);
            v8 = (v7 & 1) + 5;
            v59 = ((v7 >> 4) & 1) + 5;
            v53 = ((v7 >> 1) & 1) + 5;
            v55 = ((v7 >> 2) & 1) + 5;
            v57 = ((v7 >> 3) & 1) + 5;
            v9 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&name, 1);
            v45 = (v9 & 1) + 1;
            v51 = ((v9 >> 4) & 1) + 1;
            v47 = ((v9 >> 1) & 1) + 1;
            v10 = ((v9 >> 2) & 1) + 1;
            v49 = ((v9 >> 3) & 1) + 1;
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```
GetAt이라는 함수를 사용해서 name의 첫번째 글자와 두번째 글자를 추출했다. 그리고 각 글자에 대해서 5번의 서로 다른 연산을 해서 스택에 저장해놓고 있었다.
```
itow_s(v8 + v10, v11, 0xAu, 10);
v12 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&v63, 0);
v13 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&serial, 0);
v2 = &v63;
if ( v13 == v12 )
{
  itow_s(v57 + v49, v14, 0xAu, 10);
  v15 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&serial, 1);
  v16 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&v63, 0);
  v2 = &v63;
  if ( v15 == v16 )
  {
    itow_s(v53 + v51, v17, 0xAu, 10);
    v18 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&serial, 2);
    v19 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&v63, 0);
    v2 = &v63;
    if ( v18 == v19 )
    {
      itow_s(v55 + v45, v20, 0xAu, 10);
      v21 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&serial, 3);
      v22 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&v63, 0);
      v2 = &v63;
      if ( v21 == v22 )
      {
        itow_s(v59 + v47, v23, 0xAu, 10);
        v24 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&serial, 4);
        v25 = ATL::CSimpleStringT<wchar_t,1>::GetAt(&v63, 0);
        v2 = &v63;
        if ( v24 == v25 )
        {
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```
제일 처음 연산하는 부분을 보면 v57과 v49를 더한 숫자와 serial의 첫번째 숫자와 비교를 하고 있었다. 나머지도 마찬가지로 name의 첫번째 글자와 두번째 글자로 연산한 값들 중에서 2개를 더한 값과 serial을 비교하고 있었다.
이후에도 name의 세번째 글자와 네번째 글자로 비슷한 방식으로 검증을 하고 있는 것을 확인했다. 힌트에서 유추해보면 주어진 serial의 조건을 만족하는 name이 여러개일 것으로 추측이 된다. 따라서 이 모든 조건을 만족하는 여러개의 name을 찾으려면 엄청나게 오랜 시간이 걸린다. 따라서 해당하는 name을 찾는 코드를 작성해서 풀기로 했다.
```python
import sys

print "[start]\n"

for n1 in range(0x61,0x7b):
    for n2 in range(0x61,0x7b):
        v8 = (n1 & 1) + 5
        v53 = ((n1 >> 1) & 1) + 5
        v55 = ((n1 >> 2) & 1) + 5
        v57 = ((n1 >> 3) & 1) + 5
        v59 = ((n1 >> 4) & 1) + 5

        v45 = (n2 & 1) + 1
        v47 = ((n2 >> 1) & 1) + 1
        v10 = ((n2 >> 2) & 1) + 1
        v49 = ((n2 >> 3) & 1) + 1
        v51 = ((n2 >> 4) & 1) + 1

        if(((v8 + v10)==7)and((v49 + v57)==6)and((v53 + v51)==8)and((v55 + v45)==7)and((v59 + v47)==6)):
            sys.stdout.write(chr(n1)+chr(n2))

            for n3 in range(0x61,0x7b):
                for n4 in range(0x61,0x7b):
                    v27 = (n3 & 1) + 5
                    v60 = ((n3 >> 4) & 1) + 5
                    v54 = ((n3 >> 1) & 1) + 5
                    v56 = ((n3 >> 2) & 1) + 5
                    v58 = ((n3 >> 3) & 1) + 5

                    v46 = (n4 & 1) + 1
                    v52 = ((n4 >> 4) & 1) + 1
                    v48 = ((n4 >> 1) & 1) + 1
                    v29 = ((n4 >> 2) & 1) + 1
                    v50 = ((n4 >> 3) & 1) + 1

                    if(((v27 + v29)==7)and((v58 + v50)==7)and((v54 + v52)==7)and((v56 + v46)==7)and((v60 + v48)==6)):
                        if(n4==112):
                            print chr(n3)+chr(n4)
# python exploit.py
[start]

bump
cqmp
ftmp
gpmp
```
코드를 돌려서 4개의 문자를 추출했다. 4개의 문자 모두 Position.exe에서는 Correct!가 나왔지만 reversing.kr의 auth에는 bump만이 인증이 되었다.
답 : bump