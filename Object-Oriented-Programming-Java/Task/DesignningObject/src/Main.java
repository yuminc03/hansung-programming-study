// 슈퍼 클래스 설계
// 모바일 앱이나 프로그램의 화면을 구성하는 시각적 요소들 - UI 컴포넌트
class UIComponent {
    protected double x; // X 좌표
    protected double y; // Y 좌표
    protected int width; // 너비
    protected int height; // 높이

    // 컴포넌트의 위치와 크기를 설정
    public void setFrame(double x, double y, int width, int height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    // 화면에 UI 요소를 그리기 - 서브 클래스에서 재정의할 기본 메서드
    public void draw() {
        System.out.printf("기본 컴포넌트를 [%.1f, %.1f] 위치에 크기 %d X %d로 배치합니다.\n", x, y, width, height);
        // 좌표와 너비, 높이를 포맷 지정으로 출력
    }
}

// 서브 클래스 구현 및 오버라이딩 (버튼)
class RoundedButton extends UIComponent {
    private String title; // 버튼에 들어갈 텍스트
    private double cornerRadius; // 모서리의 둥근 정도

    // 생성자 - RoundedButton 속성 초기화
    public RoundedButton(String title, double cornerRadius) {
        this.title = title;
        this.cornerRadius = cornerRadius;
    }

    // ⭐️ 슈퍼 클래스의 메서드 오버라이딩
    @Override
    public void draw() {
        System.out.printf("[%.1f, %.1f] 위치에 반경 %.1f만큼 둥근 모서리를 가지고 크기가 %d X %d인 '%s' 버튼을 렌더링합니다.\n", x, y, cornerRadius, width, height, title); // 슈퍼 클래스의 속성(x, y, width, height)과 자신의 고유 속성(title, cornerRadius)을 함께 출력
    }
}

// 서브 클래스 구현 및 오버라이딩 (토글 스위치)
class ToggleSwitch extends UIComponent {
    private boolean isOn; // 스위치의 켜짐/꺼짐 상태

    // 생성자 - ToggleSwitch 속성 초기화
    public ToggleSwitch(boolean isOn) {
        this.isOn = isOn;
    }

    // ⭐️ 슈퍼 클래스의 메서드 오버라이딩
    @Override
    public void draw() {
        String stateColor = isOn ? "초록색(ON)" : "회색(OFF)"; // isOn이 true면 "초록색(ON)", false면 "회색(OFF)" 문자열을 변수에 저장
        System.out.printf("[%.1f, %.1f] 위치에 크기가 %d X %d이고 배경색이 %s인 직관적인 토글 스위치를 렌더링합니다.\n", x, y, width, height, stateColor); // 슈퍼 클래스의 속성(x, y, width, height)과 자신의 고유 속성(isOn 상태에 따른 stateColor)을 함께 출력
    }

    // 서브 클래스만의 고유 메서드
    public void toggle() {
        isOn = !isOn; // toggle 값 변경
        System.out.println("스위치 상태가 변경되었습니다. -> " + isOn);
        draw(); // 상태 변경 후 다시 그리기
    }
}

// ==========================================
// [실행 테스트를 위한 Main 클래스]
// ==========================================
public class Main {
    public static void main(String[] args) {
        // 하위 클래스의 객체 생성
        RoundedButton loginButton = new RoundedButton("로그인", 12.0);
        ToggleSwitch faceIdSwitch = new ToggleSwitch(false);

        // 슈퍼 클래스에서 상속받은 setFrame() 메서드를 호출하여 위치(x,y)와 크기(width,height)를 설정
        // x, y는 double형식(소수점), width, height는 int형식(정수)으로 입력
        loginButton.setFrame(20.0, 100.5, 300, 50);
        faceIdSwitch.setFrame(20.0, 180.0, 60, 30);

        loginButton.draw();
        // 오버라이딩된 draw() 메서드를 실행하여 loginButton을 화면에 렌더링

        faceIdSwitch.draw();
        // 오버라이딩된 draw() 메서드를 실행하여 faceIdSwitch을 화면에 렌더링

        faceIdSwitch.toggle();
        // ToggleSwitch만의 고유 기능인 toggle() 메서드를 호출하여 상태를 변경
    }
}