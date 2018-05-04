Easy_Keygen
======================

-----------------
## Description
```
//ReadMe.txt
ReversingKr KeygenMe


Find the Name when the Serial is 5B134977135E7D13
```

## 분석 및 풀이
압축파일을 받아서 해제하면 Easy Keygen.exe와 ReadMe.txt라는 파일이 나온다. ReadMe.txt라는 파일을 보면 시리얼에 해당하는 이름을 찾으라고 나온다.
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int v3; // ebp@1
  signed int i; // esi@1
  int result; // eax@6
  int v6; // [sp+0h] [bp-13Ch]@0
  int v7; // [sp+0h] [bp-13Ch]@1
  char v8; // [sp+Ch] [bp-130h]@1
  char v9; // [sp+Dh] [bp-12Fh]@1
  char v10; // [sp+Eh] [bp-12Eh]@1
  char v11; // [sp+10h] [bp-12Ch]@1
  char v12; // [sp+11h] [bp-12Bh]@1
  __int16 v13; // [sp+71h] [bp-CBh]@1
  char v14; // [sp+73h] [bp-C9h]@1
  char v15; // [sp+74h] [bp-C8h]@1
  char v16; // [sp+75h] [bp-C7h]@1
  __int16 v17; // [sp+139h] [bp-3h]@1
  char v18; // [sp+13Bh] [bp-1h]@1

  v11 = 0;
  v15 = 0;
  memset(&v12, 0, 0x60u);
  v13 = 0;
  v14 = 0;
  memset(&v16, 0, 0xC4u);
  v17 = 0;
  v18 = 0;
  v8 = 0x10;
  v9 = 0x20;
  v10 = 0x30;
  sub_4011B9((int)aInputName, v6);
  scanf(aS, &v11);
  v3 = 0;
  for ( i = 0; v3 < (signed int)strlen(&v11); ++i )
  {
    if ( i >= 3 )
      i = 0;
    sprintf(&v15, aS02x, &v15, *(&v11 + v3++) ^ *(&v8 + i));
  }
  memset(&v11, 0, 0x64u);
  sub_4011B9((int)aInputSerial, v7);
  scanf(aS, &v11);
  if ( !strcmp(&v11, &v15) )
  {
    sub_4011B9((int)aCorrect, *(int *)&v8);
    result = 0;
  }
  else
  {
    sub_4011B9((int)aWrong, *(int *)&v8);
    result = 0;
  }
  return result;
}
```
메인 함수를 보면 다음과 같다. 분석해보면 출력을 해주는 printf와 같은 함수는 존재하지 않는다. 대신 sub_401B9함수가 출력을 담당햊는 함수인듯 하다. scanf로 v11에 이름을 입력받고 입력받은 문장을 갖고 for문에서 특정 연산을 진행한 후 v15에 저장한다. 그 후 v11을 초기화한 후 시리얼 넘버를 다시 v11에 입력을 받고 v15와 비교한다. 
```
int sprintf(char *a1, const char *a2, ...)
{
.............
  v2 = sub_401427(&v6, (int)a2, (int)va);
.............
}
int ___cdecl sub_4011B9(int a1, int a2)
{
...........
  v2 = _stbuf((int)&stru_4080B0);
  v3 = sub_401427(&stru_4080B0, a1, (int)&a2);
  _ftbuf(v2, (int)&stru_4080B0);
  return v3;
...........
}
```
좀 더 분석을 해보니 sprintf와 sub_4011B9함수 둘다 결국은 sub_401427함수를 호출하였다. 차이점은 sub_401427함수내에서 확인이 가능하다. sub_4011B9함수는 무조건 sub_401427함수내에 case 0으로 갔고 sprintf에서는 case 0으로 가지 않았다. 결국 미리 저장된 offset의 값을 출력하느냐 아니냐의 차이에 따라서 다르게 움직이고 있었다.
```
sprintf(&v15, aS02x, &v15, *(&v11 + v3++) ^ *(&v8 + i));
//*(&v11 + v3++) ^ *(&v8 + i) 이 연산이 이 문제의 핵심
```
sub_401427같이 복잡하고 긴 함수들이 쓰였지만 이 문제를 푸는데 결국 핵심은 sprintf이다.
(&v11 + v3++)는 입력받은 이름을 배열에 저장하고 각 문자의 위치를 나타내준다.
ex) char a[] = "hello" => &v11+0 = "h", &v11+1 = "e" 등등
(&v8 + i)는 v8, v9, v10이 각각 0x10, 0x20, 0x30을 순서대로 저장되있기 때문에 i가 값이 뭐냐에 따라서 앞의 값과 0x10, 0x20, 0x30으로 xor연산을 시켜준다. 그리고 이 세 숫자만을 사용할 것이기 때문에 if문으로 i를 초기화해줬다.
```
input name :    aabbcc          //616162626363 ^ 102030102030
input serial :  714152724353
Correct!
-----------------------------------------
Input Name: K3yg3nm3
Input Serial: 5B134977135E7D13
Correct!
```
aabbcc에 해당하는 시리얼 넘버를 넣어봤고 "Correct!"라는 문구가 떴다. 그렇지만 우리는 5B134977135E7D13라는 시리얼에 해당하는 이름이 필요하다. 역연산을 해보면 이름은 K3yg3nm3라는 것을 알 수 있다.


##풀이 2
```
.text:0040107E movsx   ecx, [esp+esi+13Ch+var_130]	//10h, 20h, 30h가 순서대로 저장
.text:00401083 movsx   edx, [esp+ebp+13Ch+var_12C]	//입력한 name이 저장
.text:00401088 xor     ecx, edx					   //xor 연산
.text:0040108A lea     eax, [esp+13Ch+var_C8]		 //연산 결과를 이 위치에 저장
.text:0040108E push    ecx
.text:0040108F push    eax
.text:00401090 lea     ecx, [esp+144h+var_C8]		
.text:00401094 push    offset aS02x    ; "%s%02X"
.text:00401099 push    ecx             ; char *
.text:0040109A call    _sprintf
----------------------------------------------------------------------------------------
.text:004010E2 lea     esi, [esp+13Ch+var_C8]       // 연산 결과
.text:004010E6 lea     eax, [esp+13Ch+var_12C]      // 입력받은 시리얼 넘버
.text:004010EA
.text:004010EA loc_4010EA:                             ; CODE XREF: _main+108j
.text:004010EA mov     dl, [eax]
.text:004010EC mov     cl, dl
.text:004010EE cmp     dl, [esi]					// 결과 비교
.text:004010F0 jnz     short loc_40110E
```
ida가 아니라 ollydbg같이 어셈블리어만 보고 분석해봤다. 역시 sprintf를 보면 알 수 있기에 동적으로 분석해봤다.
[esp+esi+13Ch+var_130]의 값이 10h, 20h, 30h가 순차적으로 나오는 것을 알 수 있다. 
[esp+ebp+13Ch+var_12C]의 값은 입력한 name이 저장되있는 것을 확인할 수 있다.
[esp+13Ch+var_C8]은 위의 두 값을 xor연산을 한 결과를 저장하는 것을 알 수 있다.
결론적으로 주어진 시리얼 넘버를 갖고 10h, 20h, 30h와 역연산을 해보면 name을 찾을 수 있다.

## 번외
```C
#include<stdio.h>
#include<string.h>

int main() {

    int i,v=0,j;
    int n[3]={16,32,48};
    char str[10];
    char buf[20];

    memset(str,0,strlen(str));
    memset(buf,0,strlen(buf));
    printf("%s\n",str);

    printf("Input Name : ");
    scanf("%s",str);


    for(i=0; v<strlen(str);i++)
    {
        if(i>=3){
            i=0;
        }

        sprintf(buf,"%s%2x\n",buf,*(str + v) ^ n[i]);
        buf[strlen(buf) -1] = '\0';
        ++v;

    }
    memset(str,0,strlen(str));

    printf("Input Serial: ");
    scanf("%s",str);

    if(!strcmp(str,buf))
        printf("Correct!\n");
    else
        printf("Wrong!\n");

    return 0;
}
```
나름 main을 구현해보긴 했다. 알파벳이 중간에 들어갈 경우 대소문자가 반대로 나오긴 하지만 이런식으로 구현이 되있는 듯하다.