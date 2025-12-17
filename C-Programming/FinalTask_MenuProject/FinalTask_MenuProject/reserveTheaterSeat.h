#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// 좌석 예약 시스템
void reserveTheaterSeat()
{
	srand(time(NULL)); // 랜덤 함수 사용하기 위한 준비

	int i; // 좌석의 index 번호
	int a[10]; // 좌석자리 10개
	int seatNumber; // 예약할 좌석 번호

	printf("좌석번호: 1 2 3 4 5 6 7 8 9 10"); // 좌석번호 출력
	printf("\n");
	printf("예약현황: "); // 예약 현황 출력
	for (i = 0; i < 10; i++) { // 0~9까지(총 10번) 반복
		// 0: 남은 좌석, 1: 예약된 좌석
		a[i] = (rand() % 2); // a의 값을 random으로 받아, 예약된 좌석을 랜덤배치 (0 or 1)
		printf("%d ", a[i]); // 좌석 출력
	}
	printf("\n");

	while (1) { // 무한 반복 시작
		int seatCount = 0; // 예약된 좌석의 수

		// 예약할 좌석 질문
		printf("몇 번째 좌석을 예약하시겠습니까? ");
		scanf("%d", &seatNumber); // 예약할 좌석번호 입력받기

		if (a[seatNumber - 1] == 0) { // 선택한 좌석이 예약이 가능할 떄
			printf("* 예약 가능 *\n"); // '예약 가능' 출력
			a[seatNumber - 1] = 1; // 좌석을 '예약됨'으로 표시
		}
		else if (a[seatNumber - 1] == 1) { // 선택한 좌석이 예약이 불가능할 떄
			printf("* 예약 불가능 *\n"); // '예약 불가능' 출력
		}

		// 좌석 예약 후, 예약 현황 출력
		printf("좌석번호: 1 2 3 4 5 6 7 8 9 10");
		printf("\n");
		printf("예약현황: ");
		for (i = 0; i < 10; i++) { // 좌석 수만큼 반복
			printf("%d ", a[i]); // i번째 좌석 예약현황 출력
		}
		printf("\n");

		// 만석 확인
		for (int j = 0; j < 10; j++) { // 좌석 수만큼 반복
			if (a[j] == 1) { // 만약 예약된 좌석이면
				seatCount += 1; // 예약된 좌석의 수 1 증가
			}
		}
		
		if (seatCount == 10) { // 예약된 좌석이 10개면
			printf("\n만석입니다..\n"); // 만석 출력
			break; // 반복 종료
		}
	}
}