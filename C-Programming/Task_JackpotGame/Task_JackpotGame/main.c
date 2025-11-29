#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
	const int COIN = 1; // 게임 한 판에 사용할 코인의 수
	const int JACKPOT_REWARD = 80; // 잭팟 상품
	const int TRIPLE_REWARD = 40; // 트리플 상품

	srand(time(NULL));
	int attemptCount = 0; // 게임 시도 횟수
	int jackpotWins = 0; // 7-7-7 잭팟 횟수
	int tripleWins = 0; // 7-7-7 잭팟 횟수를 제외한 트리플 횟수(예시: 3-3-3)
	int coins; // 기본으로 갖고 시작할 코인의 수
	
	// 게임 시작전 게임 간단 설명
	printf("=========================================================\n");
	printf("잭팟 게임을 시작합니다! 코인이 부족하면 게임이 종료됩니다.\n");
	printf("게임 한 판에 사용할 코인은 %d개 입니다.\n", COIN);
	printf("게임을 할 때 사용할 코인 개수를 입력하세요: ");
	scanf("%d", &coins); // 사용할 코인 개수 입력받기
	printf("=========================================================\n");
	printf("\n");

	do {
		coins -= COIN; // 코인 감소
		attemptCount += 1; // 시도 횟수 1 증가

		// 현재 게임 시도 현황 (시도 횟수, 남은 코인)
		printf("==============%d회 게임==============\n", attemptCount);
		printf("===========남은 코인: %d개===========\n", coins);
		int num1 = (rand() % 7) + 1; // 1번째 숫자 뽑기
		int num2 = (rand() % 7) + 1; // 2번째 숫자 뽑기
		int num3 = (rand() % 7) + 1; // 3번째 숫자 뽑기
		// 게임 결과 출력
		printf("======%d회 게임 결과: [%d] [%d] [%d]======\n", attemptCount, num1, num2, num3);

		// 숫자 3개가 모두 7일 때 (잭팟 당첨)
		if (num1 == 7 && num2 == 7 && num3 == 7)
		{
			// 잭팟 (7-7-7)
			printf("\n\n");
			printf("***********************************************\n");
			printf("<<-------    %d-%d-%d 잭팟 성공!    ------->>\n", num1, num2, num3);
			printf("<<-------   게임 시도 횟수: %d   -------->>\n", attemptCount);
			printf("<<-------     + %d 코인!    ------->>\n", JACKPOT_REWARD);
			printf("***********************************************\n");
			printf("\n");
			
			// 잭팟 상품만큼 코인 충전, 잭팟 횟수 1 증가
			coins += JACKPOT_REWARD;
			jackpotWins += 1;
		}
		else if (num1 == num2 && num2 == num3) {
			// 잭팟이 아닌 트리플 (3-3-3, 5-5-5 등..)
			printf("\n\n");
			printf("********************************************\n");
			printf("<<-------    %d-%d-%d 트리플!    ------->>\n", num1, num2, num3);
			printf("<<-------      + %d 코인!     -------->>\n", TRIPLE_REWARD);
			printf("<<------ 게임 시도 횟수: %d ------>>\n", attemptCount);
			printf("********************************************\n");
			printf("\n");

			// 트리플 상품만큼 코인 충전, 트리플 횟수 1 증가
			coins += TRIPLE_REWARD;
			tripleWins += 1;
		}
		else {
			// 아무것도 당첨되지 않음
			printf("다음 기회에..\n");
		} // end if

		// 사용할 코인보다 현재 코인이 적게 남았을 때, 게임 종료
		if (coins < COIN) {
			printf("<<---코인이 부족해서 게임을 계속할 수 없습니다.. --->>\n");
			break;
		}
	} while (coins > 0); // 코인이 0보다 많이 남을 때까지 반복

	// 잭팟 게임 결과 출력
	printf("\n\n");
	printf("=========================================================\n");
	printf("         ** 잭팟 게임 결과가 나왔습니다! **\n");
	printf("---------------------------------------------------------\n");
	printf("게임을 하는 동안, 총 %d번 시도했습니다.\n\n", attemptCount);
	printf("----------------------당첨된 기록------------------------\n");
	printf("잭팟: %d번\n", jackpotWins);
	printf("잭팟이 아닌 트리플 (ex: 1-1-1): %d번\n", tripleWins);
	printf("=========================================================\n");
	
	return 0;
}