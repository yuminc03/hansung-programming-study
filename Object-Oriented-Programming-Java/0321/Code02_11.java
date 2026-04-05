import java.util.Scanner;

public class Code02_11 {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        
        double num;

        System.out.print("실수 입력: ");
        num = s.nextDouble();
        System.out.println("사용자가 입력한 값: " + num);

        String str;
        System.out.print("문자열 입력: ");
        str = s.next();
        System.out.println("사용자가 입력한 값: " + str);

        s.close();
    }
}