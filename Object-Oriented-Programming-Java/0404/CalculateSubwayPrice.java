import java.util.Scanner;

// 지하철 요금 계산하기
public class CalculateSubwayPrice {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        
        int age; // 만 나이
        int price; // 요금

        System.out.print("만 나이 입력: ");
        age = s.nextInt();
        
        if (age <= 6 || age >= 65) { // 유아 (6세 이하) 또는 노인 (65세 이상)
            price = 0;
        }
        else if (age <= 13) { // 어린이 (7세 이상 13세 이하)
            price = 550;
        }
        else if (age <= 18) { // 청소년 (14세 이상 18세 이하)
            price = 900;
        }
        else { // 성인 (19세 이상 64세 이하)
            price = 1550;
        }

        if (price > 0) {
            System.out.println("지하철 요금은 " + price + "원입니다.");
        } else {
            System.out.println("지하철 요금은 무료입니다.");
        }

        s.close();
    }
}