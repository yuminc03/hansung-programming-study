#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

// 별 찍기
void printStar()
{
	// i: 별 탑의 행(탑의 층 수)
	// j: 별 탑의 열(한 층에 최대로 찍을 별 개수)
	int i, j;
	int layer; // 출력할 별의 층 수
	
	printf("출력할 별의 층 수를 입력하세요: ");
	scanf("%d", &layer); // 층 수를 입력받아, 저장

	if (layer < 1) { // 만약 layer가 1미만이면
		layer = 1; // layer에 1 대입
	}

	for (i = 0; i < layer; i++) { // i는 layer번 반복
		for (j = 0; j < layer; j++) { // j는 layer번 반복
			if (i >= j) { // 만약 i가 j 이상이면
				printf("*"); // 별 출력
			}
		}
		printf("\n"); // j 반복이 끝나면 줄바꿈
	}
}