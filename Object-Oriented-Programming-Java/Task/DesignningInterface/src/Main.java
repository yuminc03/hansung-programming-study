// 전사 역할을 수행하며 플레이어 캐릭터, 이동 가능, 공격 가능 인터페이스를 다중 구현하는 클래스
class Warrior implements PlayableCharacter, Movable, Attackable {
    // 캐릭터의 이름을 저장하는 캡슐화된 인스턴스 변수
    private String name;
    // 캐릭터의 현재 마나(MP)를 저장하는 캡슐화된 인스턴스 변수 (기존 hp를 mp로 변경)
    private int mp;

    // 전사 객체를 생성하며 이름과 마나를 초기화하는 생성자
    public Warrior(String name, int mp) {
        // 매개변수로 받은 이름을 멤버 변수 name에 저장
        this.name = name;
        // 매개변수로 받은 마나를 멤버 변수 mp에 저장
        this.mp = mp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 전사의 이동 방식을 정의
    @Override
    public void move() {
        // 콘솔에 전사의 묵직한 이동 상태를 출력
        System.out.println(name + "(전사)이(가) 무거운 갑옷을 입고 묵직하게 걸어갑니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 전사 고유 공격 멘트 출력 및 자신의 마나 소모
    @Override
    public void attack() {
        // 공격 행위로 인해 자신의 마나(MP)를 10 소모하며, 0 미만으로 내려가지 않도록 최댓값 방어 처리
        this.mp = Math.max(0, this.mp - 10);
        // 콘솔에 공격 메시지와 자신의 소모된 마나 결과를 출력
        System.out.println(name + "(전사)이(가) 검을 휘둘러 공격합니다! (자신의 MP 10 소모, 현재 MP: " + mp + ")");
    }

    // PlayableCharacter 인터페이스의 useSkill 메서드를 오버라이딩하여 전사 고유 스킬 동작을 출력
    @Override
    public void useSkill() {
        // 콘솔에 전사 고유 스킬인 휠윈드 사용 메시지 출력
        System.out.println(name + "(전사)이(가) 휠윈드(Wheelwind) 스킬을 시전합니다!");
    }

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 캐릭터의 상세 상태 정보를 조회
    @Override
    public void showStatus() {
        // 콘솔에 전사 캐릭터의 이름과 현재 마나 정보를 출력
        System.out.println("[이름: " + name + " | 직업: 전사 | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 외부로부터의 마나 감소 피해 계산 및 기록
    @Override
    public void takeDamage(int damage) {
        // Math.max를 활용하여 피해를 입은 마나가 최소 0 아래로 떨어지지 않도록 설계 (마나 번/소실 개념)
        this.mp = Math.max(0, this.mp - damage);
        // 콘솔에 마법적 피해량과 감소된 현재 마나를 실시간으로 출력
        System.out.println(name + "이(가) 외부 충격으로 " + damage + "만큼의 마나를 소실했습니다. (현재 마나: " + mp + ")");
    }

    // 캐릭터의 이름을 반환하는 Getter 메서드 오버라이딩
    @Override
    public String getName() { 
        // 멤버 변수 name을 외부로 안전하게 반환
        return name; 
    }
}

// 마법사 역할을 수행하며 플레이어 캐릭터, 이동 가능, 공격 가능 인터페이스를 다중 구현하는 클래스
class Wizard implements PlayableCharacter, Movable, Attackable {
    // 마법사의 이름을 관리하는 private 캡슐화 인스턴스 변수
    private String name;
    // 마법사의 마나(MP)를 관리하는 private 캡슐화 인스턴스 변수 (기존 hp를 mp로 변경)
    private int mp;

    // 마법사 객체를 생성하며 이름과 마나를 초기화하는 생성자
    public Wizard(String name, int mp) {
        // 매개변수 name을 멤버 변수 name에 할당
        this.name = name;
        // 매개변수 mp를 멤버 변수 mp에 할당
        this.mp = mp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 마법사만의 부드러운 이동 정의
    @Override
    public void move() {
        // 콘솔에 순간이동 기반의 마법사 이동 패턴 메시지 출력
        System.out.println(name + "(마법사)이(가) 부드럽게 순간이동하며 신속하게 이동합니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 마법사 공격 멘트 출력 및 자신의 마나 소모
    @Override
    public void attack() {
        // 마법 캐스팅으로 인해 자신의 마나(MP)를 15 소모하며, 0 미만으로 떨어지지 않도록 방어 처리
        this.mp = Math.max(0, this.mp - 15);
        // 콘솔에 마법 발사 메시지와 자신의 소모된 마나 결과를 출력
        System.out.println(name + "(마법사)이(가) 강력한 파이어볼을 발사합니다! (자신의 MP 15 소모, 현재 MP: " + mp + ")");
    }

    // PlayableCharacter 인터페이스의 useSkill 메서드를 오버라이딩하여 고유 마법 시전 출력
    @Override
    public void useSkill() {
        // 마법사 광역 스킬인 블리자드 시전 로그 출력
        System.out.println(name + "(마법사)이(가) 눈보라를 퍼붓는 블리자드(Blizzard) 마법을 시전합니다!");
    }

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 마법사의 현재 상태 정보 조회
    @Override
    public void showStatus() {
        // 콘솔에 마법사 캐릭터의 현재 마나 정보를 출력
        System.out.println("[이름: " + name + " | 직업: 마법사 | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 외부로부터의 마나 감소 피해 계산 및 기록
    @Override
    public void takeDamage(int damage) {
        // 피해량 만큼 마나 감산 적용
        this.mp = Math.max(0, this.mp - damage);
        // 피해 내역 및 남은 마나 수치를 콘솔에 출력
        System.out.println(name + "이(가) 외부 충격으로 " + damage + "만큼의 마나를 소실했습니다. (현재 마나: " + mp + ")");
    }

    // 마법사의 이름을 조회하는 메서드 오버라이딩
    @Override
    public String getName() { 
        // 멤버 변수 name 반환
        return name; 
    }
}

// 궁수 역할을 수행하며 플레이어 캐릭터, 이동 가능, 공격 가능 인터페이스를 다중 구현하는 클래스
class Archer implements PlayableCharacter, Movable, Attackable {
    // 궁수의 이름을 나타내는 private 변수
    private String name;
    // 궁수의 마나(MP)를 나타내는 private 변수 (기존 hp를 mp로 변경)
    private int mp;

    // 궁수 객체를 생성하고 초기 상태를 바인딩하는 생성자
    public Archer(String name, int mp) {
        // 생성자 매개변수 name을 멤버 변수 name에 바인딩
        this.name = name;
        // 생성자 매개변수 mp를 멤버 변수 mp에 바인딩
        this.mp = mp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 궁수의 민첩한 이동 정의
    @Override
    public void move() {
        // 궁수의 나무 질주 패턴 콘솔 출력
        System.out.println(name + "(궁수)이(가) 민첩한 발걸음으로 장애물을 뛰어넘으며 질주합니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 궁수 공격 멘트 출력 및 자신의 마나 소모
    @Override
    public void attack() {
        // 화살 사격으로 인해 자신의 마나(MP)를 8 소모하며, 0 미만으로 내려가지 않도록 차단 처리
        this.mp = Math.max(0, this.mp - 8);
        // 콘솔에 사격 메시지와 자신의 소모된 마나 결과를 출력
        System.out.println(name + "(궁수)이(가) 바람의 화살을 날립니다! (자신의 MP 8 소모, 현재 MP: " + mp + ")");
    }

    // PlayableCharacter 인터페이스의 useSkill 메서드를 오버라이딩하여 멀티플 샷 기술 구현
    @Override
    public void useSkill() {
        // 궁수 광역 기술인 멀티플 샷 시전 정보 출력
        System.out.println(name + "(궁수)이(가) 공중으로 수많은 화살을 퍼붓는 멀티플 샷(Multiple Shot)을 시전합니다!");
    }

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 궁수 상태 데이터 출력
    @Override
    public void showStatus() {
        // 궁수 객체의 이름 및 마나 정보 콘솔 출력
        System.out.println("[이름: " + name + " | 직업: 궁수 | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 데미지 상쇄 및 기록
    @Override
    public void takeDamage(int damage) {
        // 피해량 만큼 마나 감산 적용
        this.mp = Math.max(0, this.mp - damage);
        // 피해 기록 및 마나 변동 이력 콘솔 출력
        System.out.println(name + "이(가) 외부 충격으로 " + damage + "만큼의 마나를 소실했습니다. (현재 마나: " + mp + ")");
    }

    // 궁수 객체의 이름을 추출하는 getter 메서드
    @Override
    public String getName() { 
        // 멤버 변수 name 반환
        return name; 
    }
}

// 다형성 행동 시뮬레이션을 실제로 가동하고 검증하는 메인 클래스
public class Main {
    // 프로그램 실행 시 최초로 호출되는 진입점 메서드
    public static void main(String[] args) {
        // 캐릭터 생성 로그를 출력
        System.out.println("=== 캐릭터 생성 및 초기 상태 ===");
        // 구체적인 전사(Warrior) 타입 변수에 전사 객체 대입 (마나 150 초기화)
        Warrior warrior = new Warrior("아라곤", 150);
        // 구체적인 마법사(Wizard) 타입 변수에 마법사 객체 대입 (마나 100 초기화)
        Wizard wizard = new Wizard("간달프", 100);
        // 구체적인 궁수(Archer) 타입 변수에 궁수 객체 대입 (마나 120 초기화)
        Archer archer = new Archer("레골라스", 120);

        // 전사 캐릭터의 현재 마나 및 세부 상태 로그 출력
        warrior.showStatus();
        // 마법사 캐릭터의 현재 마나 및 세부 상태 로그 출력
        wizard.showStatus();
        // 궁수 캐릭터의 현재 마나 및 세부 상태 로그 출력
        archer.showStatus();

        // 캐릭터들의 이동 액션 시뮬레이션을 위한 헤더 출력
        System.out.println("\n=== 이동 행동 시뮬레이션 ===");
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 move() 호출 가능
        warrior.move();
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 move() 호출 가능
        wizard.move();
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 move() 호출 가능
        archer.move();

        // 캐릭터들의 특수 스킬 사용 시뮬레이션을 위한 헤더 출력
        System.out.println("\n=== 스킬 사용 시뮬레이션 ===");
        // 전사 캐릭터의 시그니처 휠윈드 스킬 호출
        warrior.useSkill();
        // 마법사 캐릭터의 시그니처 블리자드 스킬 호출
        wizard.useSkill();
        // 궁수 캐릭터의 시그니처 멀티플 샷 스킬 호출
        archer.useSkill();

        // 다형성을 통한 실제 전투 및 피해 연산 시뮬레이션 헤더 출력 (자체 마나를 소모하는 공격)
        System.out.println("\n=== 공격 시 마나 소모 시뮬레이션 ===");
        
        // 전사가 공격하는 상황 시뮬레이션
        System.out.println("[전사 공격 행동]");
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 attack() 호출 가능 (자신의 mp 소모)
        warrior.attack();

        // 마법사가 공격하는 상황 시뮬레이션
        System.out.println("\n[마법사 공격 행동]");
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 attack() 호출 가능 (자신의 mp 소모)
        wizard.attack();

        // 궁수가 공격하는 상황 시뮬레이션
        System.out.println("\n[궁수 공격 행동]");
        // archer를 Attackable 타입으로 다운캐스팅하여 활 사격 (자신의 mp 소모)
        archer.attack();

        // 최종 상태를 검증하기 위한 콘솔 구분선 출력
        System.out.println("\n=== 최종 상태 ===");
        // 전사의 최종 상태 정보 출력
        warrior.showStatus();
        // 마법사의 최종 상태 정보 출력
        wizard.showStatus();
        // 궁수의 최종 상태 정보 출력
        archer.showStatus();
    }
}