#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
	const int COIN = 1; // 게임 한 판에 사용할 코인의 수
	const int JACKPOT_REWARD = 80; // 잭팟 상품
	const int TRIPLE_REWARD = 60; // 트리플 상품

	srand(time(NULL));
	int attemptCount = 0; // 게임 시도 횟수
	int jackpotWins = 0; // 7-7-7 잭팟 횟수 (1이 되었을 때 게임 종료)
	int tripleWins = 0; // 7-7-7 잭팟 횟수를 제외한 트리플 횟수(예시: 3-3-3)
	int coins = 100; // 기본으로 갖고 시작할 코인의 수
	
	printf("=========================================================\n");
	printf("잭팟 게임을 시작합니다! 7-7-7이 나오면 게임은 종료됩니다.\n");
	printf("게임 한 판에 사용할 코인은 %d개 입니다.\n", COIN);
	printf("=========================================================\n");
	printf("\n");

	do {
		coins -= COIN; // 코인 감소
		attemptCount += 1;

		printf("==============%d회 게임==============\n", attemptCount);
		printf("===========남은 코인: %d개===========\n", coins);
		int num1 = (rand() % 7) + 1;
		int num2 = (rand() % 7) + 1;
		int num3 = (rand() % 7) + 1;
		printf("======%d회 게임 결과: [%d] [%d] [%d]======\n", attemptCount, num1, num2, num3);

		if (num1 == 7 && num2 == 7 && num3 == 7)
		{
			// 잭팟 (7-7-7)
			printf("*************************************\n");
			printf("<<-------%d-%d-%d 잭팟 성공!------->>\n", num1, num2, num3);
			printf("<<-------게임 시도 횟수: %d-------->>\n", attemptCount);
			coins += JACKPOT_REWARD;
			jackpotWins += 1;
			printf("<<------- + %d 코인!-------->>\n", JACKPOT_REWARD);
		}
		else if (num1 == num2 && num2 == num3) {
			// 잭팟이 아닌 트리플 (3-3-3, 5-5-5 등..)
			printf("**********************************\n");
			printf("<<-------%d-%d-%d 트리플!------->>\n", num1, num2, num3);
			coins += TRIPLE_REWARD;
			tripleWins += 1;
			printf("<<------- + %d 코인!-------->>\n", TRIPLE_REWARD);
		}
		else {
			printf("다음 기회에..\n");
		} // end if

		if (coins < COIN) {
			printf("<<---코인이 부족해서 게임을 계속할 수 없습니다.. --->>\n");
			break;
		}
	} while (coins > 0);

	printf("\n\n");
	printf("=========================================================\n");
	printf("         ** 잭팟 게임 결과가 나왔습니다! **\n");
	printf("---------------------------------------------------------\n");
	printf("잭팟이 나올 때까지 총 %d번 시도했습니다.\n\n", attemptCount);
	printf("----------------------당첨된 기록------------------------\n");
	printf("잭팟이 아닌 트리플 (ex: 1-1-1): %d번\n", tripleWins);
	printf("=========================================================\n");
	
	return 0;
}