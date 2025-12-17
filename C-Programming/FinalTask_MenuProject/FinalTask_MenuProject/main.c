#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "reserveTheaterSeat.h" // 좌석 예약 시스템 header
#include "jackpotGame.h" // 잭팟 게임 header
#include "averageOfBasketballTeam.h" // 농구선수들의 키 평균 계산 header
#include "printStar.h" // 별 찍기 header

void reserveTheaterSeat(); // 좌석 예약 시스템 함수 호출 준비
void jackpotGame(); // 잭팟 게임 함수 호출 준비
void averageOfBasketballTeam(); // 농구선수들의 키 평균 계산 함수 호출 준비
void printStar(); // 별 찍기 함수 호출 준비

// 메뉴 실행 프로젝트 시작
void startMenuProject()
{
	int number; // 사용자가 입력할 메뉴 번호
	int isMenuEnded = 0; // 메뉴 프로젝트 종료 여부 (1이면 종료)

	while (isMenuEnded != 1) { // isMenuEnded가 1이 아닐 때까지 반복

		// 메뉴 실행 프로젝트 시작 후 메뉴의 종류를 설명
		printf("============================\n");
		printf("***  메뉴 실행 프로젝트  ***\n");
		printf("============================\n");
		printf("------------메뉴------------\n");
		printf("1. 좌석 예약 시스템\n");
		printf("2. 잭팟 게임\n");
		printf("3. 농구선수들의 키 평균 계산\n");
		printf("4. 별 찍기\n");
		printf("5. 종료하기\n");
		printf("============================\n");

		// 메뉴 번호 입력을 유도
		printf("\n");
		printf("실행할 메뉴의 번호를 입력하세요: ");
		scanf("%d", &number); // 사용자가 실행할 메뉴 번호 입력받기
		printf("\n");

		switch (number) { // 입력한 번호에 따라 액션 수행
		case 1: // 1번 입력한 경우
			printf("*** 좌석 예약 시스템 ***\n");
			reserveTheaterSeat(); // 좌석 예약 시스템 함수 호출
			break; // 메뉴 실행 후 switch문 빠져나가기

		case 2: // 2번 입력한 경우
			printf("*** 잭팟 게임 ***\n");
			jackpotGame(); // 잭팟 게임 함수 호출
			break; // 메뉴 실행 후 switch문 빠져나가기

		case 3: // 3번 입력한 경우
			printf("*** 농구선수들의 키 평균 계산 ***\n");
			averageOfBasketballTeam(); // 농구선수들 키 평균 계산 함수 호출
			break; // 메뉴 실행 후 switch문 빠져나가기

		case 4: // 4번 입력한 경우
			printf("*** 별 찍기 ***\n");
			printStar(); // 별 찍기 함수 호출
			break; // 메뉴 실행 후 switch문 빠져나가기

		case 5: // 5번 입력한 경우, 프로젝트 종료
			printf("메뉴 실행 프로젝트를 종료합니다 ...\n");
			break; // switch문 빠져나가기

		default: // 1~5번 외에 다른 입력인 경우, '해당번호 없음' 출력
			printf("입력한 메뉴에 해당하는 번호가 없습니다..\n");
			break; // switch문 빠져나가기
		}

		// 사용자가 종료하기(5번)나 메뉴에 없는 번호를 입력했을 때
		if (number != 1 && number != 2 && number != 3 && number != 4) {
			isMenuEnded = 1; // 메뉴 실행 프로젝트 종료
		}
	}
}

// main 함수
int main(void)
{
	startMenuProject(); // 메뉴 실행 프로젝트 시작 함수 호출

	return 0;
}