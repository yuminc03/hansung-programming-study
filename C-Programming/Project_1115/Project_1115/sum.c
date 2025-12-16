//#include <stdio.h>
//
//int main(void)
//{
//	int i, sum;
//	sum = 0;
//	int multiple = 1;
//
//	int odd = 0, even = 0;
//
//	//for (i = 1; i <= 10; i++) {
//	//	if (i % 2 == 0) {
//	//		printf("1~10에서 짝수: %d\n", i);
//	//	}
//	//}
//
//	//for (i = 0; i <= 10; i += 2) {
//	//	printf("1~10에서 짝수: %d\n", i);
//	//}
//
//	//for (i = 1; i <= 10; i++) {
//	//	if (i % 3 == 0) {
//	//		printf("1~10에서 3의 배수: %d\n", i);
//	//	}
//	//}
//
//	//for (i = 3; i <= 10; i += 3) {
//	//	printf("1~10에서 3의 배수: %d\n", i);
//	//}
//
//	//for (i = 1; i <= 10; i++) {
//	//	if (i % 5 == 0) {
//	//		printf("1~10에서 5의 배수: %d\n", i);
//	//	}
//	//}
//
//	//for (i = 5; i <= 10; i += 5) {
//	//	printf("1~10에서 5의 배수: %d\n", i);
//	//}
//
//	//for (i = 1; i <= 10; i++) {
//	//	sum += i;
//	//	multiple *= i;
//	//	printf("1부터 %d까지의 합: %d\n", i, sum);
//	//	printf("1부터 %d까지의 곱: %d\n", i, multiple);
//	//}
//
//	//printf("1부터 10까지의 정수의 합 = %d\n", sum);
//	//printf("1부터 10까지의 정수의 곱 = %d\n", multiple);
//
//	for (i = 1; i <= 10; i++) {
//		if (i % 2 == 0) {
//			even += i;
//		}
//		else {
//			odd += i;
//		}
//	}
//
//	printf("1~10까지의 짝수의 합: %d\n", even);
//	printf("1~10까지의 홀수의 합: %d\n", odd);
//
//	return 0;
//}