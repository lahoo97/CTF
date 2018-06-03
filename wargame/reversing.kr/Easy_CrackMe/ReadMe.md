Easy_CrackMe
======================


## Description
```

```

## 풀이
처음에 Easy_CrackMe 파일을 실행시키면 시리얼키를 입력하는 칸과 확인버튼이 나온다. 이 문제는 시리얼키를 입력받아서 맞는지 확인하는 문제이기 때문에 어디서인가는 비교를 하는 구문이 있어야만 한다. 그렇지만 시리얼키는 cmp로 한 문자씩 비교를 하는지 strcmp나 strncmp같은 함수를 이용해서 문자열로 비교를 하는지는 잘 모른다. 
```
.text:004010C3 sub_401080                 call    _strncmp	//1
.text:00401C48 sub_401BB5                 call    _strncmp	//2
```
ALT + t 단축기를 이용하면 Text search를 할 수 있는데 "cmp"라는 문구를 모든 바이너리 내에서 찾아봤다. 검색 결과 strncmp함수가 쓰였고 총 2번 쓰였다. 분석해보면 알수 있지만 시리얼키를 비교하는 strncmp구문은 첫번째 strncmp이다. 두번째 strncmp를 분석해보면 "____GLOBAL_HEAP_SELECTED__"라는 문구와 [ebp+Buffer]를 비교를 한다. ____GLOBAL_HEAP_SELECTED__는 ____MSVCRT_HEAP_SELECT__라는 환경변수의 값으로 ____GLOBAL_HEAP_SELECTED__로 값을 지정해주면 C 런타임이 개인힙을 사용하지 않고 OS에 할당을 요청하게 된다. 따라고 두번째 strncmp는 키값을 비교하는 함수가 아니다.
```
.text:004010B0 cmp     [esp+68h+var_63], 'a'
-------------------------------------------------------------------------------------------------
.text:004010B9 lea     ecx, [esp+6Ch+var_62]
.text:004010BD push    offset a5y      ; "5y"
.text:004010C2 push    ecx             ; char *
.text:004010C3 call    _strncmp
-------------------------------------------------------------------------------------------------
.text:004010D1 mov     esi, offset aR3versing          ; "R3versing"
.text:004010D6 lea     eax, [esp+70h+var_60]
-------------------------------------------------------------------------------------------------
.text:0040110D cmp     [esp+68h+String], 'E'
```
첫번째 strncmp를 따라가보면 해당 사용자정의 함수 내에 "Congratulation!!"과 "Incorrect Password"라는 라는 문구를 출력하는 부분이 나온다. 이 함수 내에서 문구를 비교하는데 보면 입력한 문구와 특정 문자 또는 문자열과 비교를 한다. 좀더 보기 편하게 핵심 부분만 모아서 확인을 해봤다.
```
[esp+68h+String], 'E'
[esp+68h+var_63], 'a'
[esp+6Ch+var_62], "5y"
[esp+70h+var_60], "R3versing"
//Ea5yR3versing
```
각 문구들을 비교하는 스택의 위치를 찾아서 순서대로 재배열 해봤다. 그러니까 "Ea5yR3versing"라는 문구가 나왔고 이를 입력하니까 정답이 나왔다.
