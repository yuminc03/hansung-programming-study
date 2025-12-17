#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#define COUNT 10 // 농구선수들의 수

// 농구선수들의 키 평균 계산
void averageOfBasketballTeam()
{
	int humans[COUNT]; // 농구선수들 키 (10개)
	int sum = 0; // 농구선수들 키 합계
	int i; // 농구선수 index

	// 10번 반복 (농구선수들의 인원 수만큼 반복)
	for (i = 0; i < COUNT; i++) {
		printf("%d번째 농구선수의 키 입력: ", i+1);
		scanf("%d", &humans[i]); // 10명의 키를 입력받아, 저장
	}

	// 10번 반복 (농구선수들의 인원 수만큼 반복)
	for (i = 0; i < COUNT; i++) {
		sum += humans[i]; // 농구선수들의 키를 누적합
	}

	// 농구선수들의 키 평균 계산하고 출력
	printf("농구선수들의 키 평균: %.2f\n", (float)sum / COUNT);
}