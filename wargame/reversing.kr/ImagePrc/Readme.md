ImagePrc
======================

## Description
```

```
## 분석 및 풀이
ImagePrc.exe 파일을 실행해보면 흰색 화면바탕에 Check라는 버튼이 있다. Check 버튼을 누르면 Wrong이라는 메세지 박스가 나온다.
```
 v7 = GetDC(hWnd);
 hbm = CreateCompatibleBitmap(v7, 200, 150);
 hdc = CreateCompatibleDC(v7);
 h = SelectObject(hdc, hbm);
 Rectangle(hdc, -5, -5, 205, 205);
 ReleaseDC(hWnd, v7);
 ::wParam = (WPARAM)CreateFontA(12, 0, 0, 0, 400, 0, 0, 0, 0x81u, 0, 0, 0, 0x12u, pszFaceName);
 dword_4084E0 = (int)CreateWindowExA(0, Button, Check, 0x50000000u, 60, 85, 80, 28, hWnd,   (HMENU)0x64, hInstance, 0);
 SendMessageA((HWND)dword_4084E0, 0x30u, ::wParam, 0);
 return 0;
```
처음에 프로그램이 실행되기 전에 위의 과정을 거치게 된다. Windows 운영체제에서 특정 윈도우 또는 메모리에 그림을 그리고 싶으면 DC(Device Context)가 필요하다. 그 후 GDI(graphics Device Interface)에서 제공하는 함수를 사용해서 그림을 그릴 수 있게 된다.
GetDC() - CreateCompatibleBitmap() - CreateCompatibleDC() - SelectObject() -  Rectangle() - ReleaseDC() 순으로 함수가 호출되었다. 쉬운 설명을 위해 ImagePrc.exe의 흰색 부분을 도화지라고 지칭할 것이다.
그림을 그리는 프로그램을 만들기 위한 DC를 만들어주는 함수로 _CreateCompatibleDC()_를 사용한다. 그렇지만 _CreateCompatibleDC()_ 함수를 사용해서 얻은 DC는 출력해줄 대상이 없는 상태로 그리기만 해주는 함수이다. 그래서 출력해줄 대상(도화지)를 _CreateCompatibleBitmap()_함수로 생성해줘야 한다. 따라서 _CreateCompatibleDC()_ 함수 이전에 CreateCompatibleBitmap()함수를 먼저 호출해준다. 그 후 SelectObject()함수로 그림을 그릴 장소(도화지)를 선택해준다. 그 후 Rectangle()함수로 도화지를 그리고 SendMessage()함수로 버튼과 폰트를 생성해주면 사용자한테 띄워줄 창을 완성하여 띄워준다.
```
.text:004013A3 loc_4013A3:
.text:004013A3 mov     dl, [ecx]
.text:004013A5 mov     bl, [eax+ecx]
.text:004013A8 cmp     dl, bl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      while ( *(_BYTE *)v13 == *((_BYTE *)v13 + v14) )
      {
        ++v12;
        v13 = (char *)v13 + 1;
        if ( v12 >= 90000 )
        {
          sub_401500(v8);
          return 0;
        }
      }
      MessageBoxA(hWnd, Wrong, Caption, 0x30u);
      sub_401500(v8);
      return 0;
```
이 문제의 핵심 부분은 위의 부분이다. 위의 부분을 보면 ecx에 해당하는 주소와 eax+ecx에 해당하는 주소에서 1byte씩 총 0x15F90만큼 비교를 한다. ecx와 eax+ecx에 해당하는 주소의 의미를 파악해야 Wrong으로 빠지지 않고 넘어갈 수 있을 것 같다. 동적으로 분석해보면 eax는 0x47E060으로 고정되어있었고 eax+ecx는 가변값이다. 유추해보면 eax는 원본 정답이 있는 위치이고 eax+ecx는 우리가 입력한 그림이 저장되는 부분인것 같다. 두 값이 같으면 어떤 결과가 나올지 궁금해서 eax, eax+ecx ,edi에 각각 0x47E060을 더해주고 jl분기를 넘어가봤다. 그렇지만 아무 결과도 나오지 않고 프로그램이 다시 check를 누르기전인 대기상태로 들어갔다.
```
.text:00401200 push    96h             ; cy
.text:00401205 push    0C8h            ; cx
.text:0040120A push    esi             ; hdc
.text:0040120B call    ds:CreateCompatible
```
flag값이 분기를 넘어가야 나오는게 아니라 그림 자체가 flag값임을 가정해봤다. 그래서 그림판으로 200(C8)x100(96)의 비트맵 그림파일을 하나 만들었다. 그 후 HXD로 열어서 0x47E060~0x493FF0까지의 바이너리값을 복사해서 붙여넣어줬다. 그렇게 하니까 이미지가 출력이 되었다.
답 : GOT