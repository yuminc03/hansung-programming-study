// 전사 역할을 수행하며 플레이어 캐릭터, 이동 가능, 공격 가능 인터페이스를 다중 구현하는 클래스
class Warrior implements PlayableCharacter, Movable, Attackable {
    // 캐릭터의 이름을 저장하는 캡슐화된 인스턴스 변수
    private String name;
    // 캐릭터의 현재 체력을 저장하는 캡슐화된 인스턴스 변수
    private int hp;

    // 전사 객체를 생성하며 이름과 체력을 초기화하는 생성자
    public Warrior(String name, int hp) {
        // 매개변수로 받은 이름을 멤버 변수 name에 저장
        this.name = name;
        // 매개변수로 받은 체력을 멤버 변수 hp에 저장
        this.hp = hp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 전사의 이동 방식을 정의
    @Override
    public void move() {
        // 콘솔에 전사의 묵직한 이동 상태를 출력
        System.out.println(name + "(전사)이(가) 무거운 갑옷을 입고 묵직하게 걸어갑니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 전사 고유 공격 멘트 출력 (인자 없음)
    @Override
    public void attack() {
        // 콘솔에 전사의 물리 일반 공격 메시지를 출력
        System.out.println(name + "(전사)이(가) 검을 넓게 휘두르며 강력하게 베어냅니다! (기본 피해량: 15)");
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
        // 콘솔에 전사 캐릭터의 이름과 현재 체력 정보를 출력
        System.out.println("[이름: " + name + " | 직업: 전사 | 체력: " + hp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 데미지를 차감하고 체력 무결성을 검증
    @Override
    public void takeDamage(int damage) {
        // Math.max를 활용하여 데미지를 뺀 체력이 최소 0 아래로 떨어지지 않도록 설계
        this.hp = Math.max(0, this.hp - damage);
        // 콘솔에 피해량과 감소된 현재 체력을 실시간으로 출력
        System.out.println(name + "이(가) " + damage + "의 피해를 입었습니다. (현재 체력: " + hp + ")");
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
    // 마법사의 체력을 관리하는 private 캡슐화 인스턴스 변수
    private int hp;

    // 마법사 객체를 생성하며 이름과 체력을 초기화하는 생성자
    public Wizard(String name, int hp) {
        // 매개변수 name을 멤버 변수 name에 할당
        this.name = name;
        // 매개변수 hp를 멤버 변수 hp에 할당
        this.hp = hp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 마법사만의 부드러운 이동 정의
    @Override
    public void move() {
        // 콘솔에 순간이동 기반의 마법사 이동 패턴 메시지 출력
        System.out.println(name + "(마법사)이(가) 부드럽게 순간이동하며 신속하게 이동합니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 마법사 공격 멘트 출력 (인자 없음)
    @Override
    public void attack() {
        // 파이어볼 마법으로 일반 공격을 한다는 로그 출력
        System.out.println(name + "(마법사)이(가) 전방을 향해 불타오르는 파이어볼 마법을 발사합니다! (기본 피해량: 25)");
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
        // 콘솔에 마법사 캐릭터의 현재 상태값들 출력
        System.out.println("[이름: " + name + " | 직업: 마법사 | 체력: " + hp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 피해 계산 및 생존 상태 실시간 기록
    @Override
    public void takeDamage(int damage) {
        // 0 미만의 음수 체력이 발생하지 않도록 체력 조절 로직 적용
        this.hp = Math.max(0, this.hp - damage);
        // 피해 내역 및 남은 체력 수치를 콘솔에 출력
        System.out.println(name + "이(가) " + damage + "의 피해를 입었습니다. (현재 체력: " + hp + ")");
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
    // 궁수의 체력을 나타내는 private 변수
    private int hp;

    // 궁수 객체를 생성하고 초기 상태를 바인딩하는 생성자
    public Archer(String name, int hp) {
        // 생성자 매개변수 name을 멤버 변수 name에 바인딩
        this.name = name;
        // 생성자 매개변수 hp를 멤버 변수 hp에 바인딩
        this.hp = hp;
    }

    // Movable 인터페이스의 move 메서드를 오버라이딩하여 궁수의 민첩한 이동 정의
    @Override
    public void move() {
        // 궁수의 나무 질주 패턴 콘솔 출력
        System.out.println(name + "(궁수)이(가) 민첩한 발걸음으로 장애물을 뛰어넘으며 질주합니다.");
    }

    // Attackable 인터페이스의 attack 메서드를 오버라이딩하여 궁수 공격 멘트 출력 (인자 없음)
    @Override
    public void attack() {
        // 정밀 활 쏘기 공격 로그 출력
        System.out.println(name + "(궁수)이(가) 활시위를 강하게 당겨 날카로운 바람의 화살을 날립니다! (기본 피해량: 18)");
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
        // 궁수 객체의 정보 콘솔 출력
        System.out.println("[이름: " + name + " | 직업: 궁수 | 체력: " + hp + "]");
    }

    // PlayableCharacter 인터페이스의 takeDamage 메서드를 오버라이딩하여 데미지 상쇄 및 기록
    @Override
    public void takeDamage(int damage) {
        // 0 체력 보호 장치를 갖추어 궁수의 체력 감산 적용
        this.hp = Math.max(0, this.hp - damage);
        // 피해 기록 및 체력 변동 이력 콘솔 출력
        System.out.println(name + "이(가) " + damage + "의 피해를 입었습니다. (현재 체력: " + hp + ")");
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
        // PlayableCharacter 인터페이스 타입 변수에 전사(Warrior) 객체 대입 (다형성 및 업캐스팅)
        PlayableCharacter warrior = new Warrior("아라곤", 150);
        // PlayableCharacter 인터페이스 타입 변수에 마법사(Wizard) 객체 대입 (다형성 및 업캐스팅)
        PlayableCharacter wizard = new Wizard("간달프", 100);
        // PlayableCharacter 인터페이스 타입 변수에 궁수(Archer) 객체 대입 (다형성 및 업캐스팅)
        PlayableCharacter archer = new Archer("레골라스", 120);

        // 전사 캐릭터의 현재 체력 및 세부 상태 로그 출력
        warrior.showStatus();
        // 마법사 캐릭터의 현재 체력 및 세부 상태 로그 출력
        wizard.showStatus();
        // 궁수 캐릭터의 현재 체력 및 세부 상태 로그 출력
        archer.showStatus();

        // 캐릭터들의 이동 액션 시뮬레이션을 위한 헤더 출력
        System.out.println("\n=== 이동 행동 시뮬레이션 ===");
        // warrior 객체를 Movable 타입으로 형변환하여 전사 특화 이동 메서드 실행
        ((Movable)warrior).move();
        // wizard 객체를 Movable 타입으로 형변환하여 마법사 특화 이동 메서드 실행
        ((Movable)wizard).move();
        // archer 객체를 Movable 타입으로 형변환하여 궁수 특화 이동 메서드 실행
        ((Movable)archer).move();

        // 캐릭터들의 특수 스킬 사용 시뮬레이션을 위한 헤더 출력
        System.out.println("\n=== 스킬 사용 시뮬레이션 ===");
        // 전사 캐릭터의 시그니처 휠윈드 스킬 호출
        warrior.useSkill();
        // 마법사 캐릭터의 시그니처 블리자드 스킬 호출
        wizard.useSkill();
        // 궁수 캐릭터의 시그니처 멀티플 샷 스킬 호출
        archer.useSkill();

        // 다형성을 통한 실제 전투 및 피해 연산 시뮬레이션 헤더 출력 (매개변수 제거 및 직접 피해 제어)
        System.out.println("\n=== 전투 상호작용 시뮬레이션 ===");
        
        // 전사가 마법사를 공격하는 상황 시뮬레이션
        System.out.println("[전사 -> 마법사 공격]");
        // warrior를 Attackable 타입으로 다운캐스팅하여 공격 모션 가동
        ((Attackable)warrior).attack();
        // 마법사 객체의 takeDamage를 직접 실행하여 물리 피해 15를 가함
        wizard.takeDamage(15);
        // 피해 반영 결과 정보 출력
        wizard.showStatus();

        // 마법사가 궁수를 공격하는 상황 시뮬레이션
        System.out.println("\n[마법사 -> 궁수 공격]");
        // wizard를 Attackable 타입으로 다운캐스팅하여 마법 발사
        ((Attackable)wizard).attack();
        // 궁수 객체의 takeDamage를 직접 실행하여 마법 피해 25를 가함
        archer.takeDamage(25);
        // 피해 반영 결과 정보 출력
        archer.showStatus();

        // 궁수가 전사를 공격하는 상황 시뮬레이션
        System.out.println("\n[궁수 -> 전사 공격]");
        // archer를 Attackable 타입으로 다운캐스팅하여 화살 발사
        ((Attackable)archer).attack();
        // 전사 객체의 takeDamage를 직접 실행하여 원거리 화살 피해 18을 가함
        warrior.takeDamage(18);
        // 피해 반영 결과 정보 출력
        warrior.showStatus();
    }
}