#include <stdio.h>

int main(void)
{
	int i, j;

	/*
	for (i = 0; i <= 5; i++) {
		for (j = 0; j <= 3; j++) {
			printf("i: %d, j: %d\n", i, j);
		}
	}
	*/

	// º° ´Ù¼¸°³¾¿ 5ÁÙ Âï±â

	for (i = 0; i < 5; i++) {
		for (j = 0; j < 5; j++) {
			printf("*");
		}
		printf("\n");
	}

	printf("\n");

	for (int a = 1; a <= 5; a++) {
		for (int b = 1; b <= 5; b++) {
			if (a >= b) {
				printf("*");
			}
		}
		printf("\n");
	}

	return 0;
}