// 전사 역할을 수행하며 플레이어 캐릭터, 이동 가능, 공격 가능 인터페이스를 다중 구현하는 클래스
class Warrior implements PlayableCharacter, Movable, Attackable {
    // 캐릭터의 이름을 저장하는 캡슐화된 인스턴스 변수
    private String name;
    // 캐릭터의 현재 체력(HP)을 저장하는 캡슐화된 인스턴스 변수 (hp 필드 도입)
    private int hp;
    // 캐릭터의 현재 마나(MP)를 저장하는 캡슐화된 인스턴스 변수
    private int mp;

    // 전사 객체를 생성하며 이름, 체력, 마나를 초기화하는 생성자 (hp 파라미터 추가)
    Warrior(String name, int hp, int mp) {
        // 매개변수로 받은 이름을 멤버 변수 name에 저장
        this.name = name;
        // 매개변수로 받은 체력을 멤버 변수 hp에 저장
        this.hp = hp;
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

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 캐릭터의 상세 상태 정보를 조회 (HP와 MP 모두 출력)
    @Override
    public void showStatus() {
        // 콘솔에 전사 캐릭터의 이름, 현재 체력, 현재 마나 정보를 출력
        System.out.println("[이름: " + name + " | 직업: 전사 | 체력(HP): " + hp + " | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 외부 피해만큼 실제 체력(HP)을 감소시키고 기록
    @Override
    public void takeDamage(int damage) {
        // Math.max를 활용하여 데미지를 뺀 체력이 최소 0 아래로 떨어지지 않도록 설계 (hp 차감 적용)
        this.hp = Math.max(0, this.hp - damage);
        // 콘솔에 외부 피해량과 감소된 현재 체력을 실시간으로 출력
        System.out.println(name + "이(가) 외부로부터 " + damage + "만큼의 피해를 입었습니다. (현재 체력: " + hp + ")");
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
    // 마법사의 이름
    private String name;
    // 마법사의 체력을 관리하는 private 캡슐화 인스턴스 변수 (hp 필드 도입)
    private int hp;
    // 마법사의 마나(MP)를 관리하는 private 캡슐화 인스턴스 변수
    private int mp;

    // 마법사 객체를 생성하며 이름, 체력, 마나를 초기화하는 생성자 (hp 파라미터 추가)
    Wizard(String name, int hp, int mp) {
        // 매개변수 name을 멤버 변수 name에 할당
        this.name = name;
        // 매개변수 hp를 멤버 변수 hp에 할당
        this.hp = hp;
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

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 마법사의 현재 상태 정보 조회 (HP와 MP 모두 출력)
    @Override
    public void showStatus() {
        // 콘솔에 마법사 캐릭터의 이름, 현재 체력, 현재 마나 정보를 출력
        System.out.println("[이름: " + name + " | 직업: 마법사 | 체력(HP): " + hp + " | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 외부 피해만큼 실제 체력(HP)을 감소시키고 기록
    @Override
    public void takeDamage(int damage) {
        // 피해량 만큼 체력(HP) 감산 적용
        this.hp = Math.max(0, this.hp - damage);
        // 피해 내역 및 남은 체력 수치를 콘솔에 출력
        System.out.println(name + "이(가) 외부로부터 " + damage + "만큼의 피해를 입었습니다. (현재 체력: " + hp + ")");
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
    // 궁수의 이름
    private String name;
    // 궁수의 체력을 나타내는 private 변수 (hp 필드 도입)
    private int hp;
    // 궁수의 마나(MP)를 나타내는 private 변수
    private int mp;

    // 궁수 객체를 생성하고 초기 상태를 바인딩하는 생성자 (hp 파라미터 추가)
    Archer(String name, int hp, int mp) {
        // 생성자 매개변수 name을 멤버 변수 name에 바인딩
        this.name = name;
        // 생성자 매개변수 hp를 멤버 변수 hp에 바인딩
        this.hp = hp;
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

    // PlayableCharacter 인터페이스의 showStatus 메서드를 오버라이딩하여 궁수 상태 데이터 출력 (HP와 MP 모두 출력)
    @Override
    public void showStatus() {
        // 궁수 객체의 이름, 체력, 마나 정보 콘솔 출력
        System.out.println("[이름: " + name + " | 직업: 궁수 | 체력(HP): " + hp + " | 마나(MP): " + mp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 데미지 상쇄 및 기록
    @Override
    public void takeDamage(int damage) {
        // 피해량 만큼 체력(HP) 감산 적용
        this.hp = Math.max(0, this.hp - damage);
        // 피해 기록 및 체력 변동 이력 콘솔 출력
        System.out.println(name + "이(가) 외부로부터 " + damage + "만큼의 피해를 입었습니다. (현재 체력: " + hp + ")");
    }

    // 궁수 객체의 이름을 추출하는 getter 메서드
    @Override
    public String getName() { 
        // 멤버 변수 name 반환
        return name; 
    }
}

// 메인 클래스
public class Main {
    public static void main(String[] args) {
        System.out.println("=== 캐릭터 생성 및 초기 상태 ===");
        // 구체적인 전사(Warrior) 타입 변수에 전사 객체 대입 (이름, HP 200, MP 150 초기화)
        Warrior warrior = new Warrior("아라곤", 200, 150);
        // 구체적인 마법사(Wizard) 타입 변수에 마법사 객체 대입 (이름, HP 120, MP 100 초기화)
        Wizard wizard = new Wizard("간달프", 120, 100);
        // 구체적인 궁수(Archer) 타입 변수에 궁수 객체 대입 (이름, HP 140, MP 120 초기화)
        Archer archer = new Archer("레골라스", 140, 120);

        // 전사 캐릭터의 현재 상태 로그 출력
        warrior.showStatus();
        // 마법사 캐릭터의 현재 상태 로그 출력
        wizard.showStatus();
        // 궁수 캐릭터의 현재 상태 로그 출력
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
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 attack() 호출 가능 (자신의 mp 소모)
        warrior.attack();
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 attack() 호출 가능 (자신의 mp 소모)
        wizard.attack();
        // 구체 클래스 타입이므로 직접 형변환 코드 없이 attack() 호출 가능 (자신의 mp 소모)
        archer.attack();

        // 외부 피해 적용 및 체력(HP) 감소 테스트 시뮬레이션 섹션
        System.out.println("\n=== 피해 발생 및 체력(HP) 감소 시뮬레이션 ===");
        // 마법사가 30의 큰 물리 공격을 받았을 때 시뮬레이션 (takeDamage 실행)
        System.out.println("[마법사 외부 피해 발생]");
        wizard.takeDamage(30);
        wizard.showStatus();

        // 전사가 50의 궁수 원거리 화살 피해를 받았을 때 시뮬레이션 (takeDamage 실행)
        System.out.println("\n[전사 외부 피해 발생]");
        warrior.takeDamage(50);
        warrior.showStatus();

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