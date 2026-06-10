# 🎮 플레이어 캐릭터 인터페이스 설계 설명서 (INTERFACE_DESIGN)

본 문서는 플레이어 캐릭터 시스템을 객체지향적이고 확장 가능하게 설계하기 위해 정의한 인터페이스 구조와 구체 클래스 구현체의 설계 사양을 상세히 설명합니다.

---

## 1. 💡 인터페이스 설계 기획 및 의도

### 1) 설계의 근본적인 목적
*   **역할 분리 원칙 (Interface Segregation Principle, ISP) 준수**: 
    캐릭터가 수행하는 책임을 단일 인터페이스나 클래스에 모두 정의하게 되면, 이동만 가능하고 공격은 할 수 없는 비전투 캐릭터나, 반대로 이동할 수 없고 제자리에서 포격만 수행하는 오브젝트(예: 고정 포탑, 장애물)를 설계할 때 불필요한 메서드를 빈 상자 형태로 강제 구현해야 하는 비효율이 발생합니다. 이를 방지하고자 **이동(`Movable`)**, **공격(`Attackable`)**, **캐릭터 기본 관리(`PlayableCharacter`)** 단위로 역할을 나누어 결합도를 극도로 낮췄습니다.
*   **느슨한 결합 (Loose Coupling)과 개방-폐쇄 원칙 (Open-Closed Principle, OCP)**:
    이후 도적(Thief), 성직자(Priest) 등 새로운 직업군이나 전혀 다른 성격의 액터가 추가되어도, 기존 프로그램의 핵심 흐름과 인터페이스 규약을 수정하지 않고 단순히 인터페이스를 다중 구현하는 신규 클래스를 추가하는 것만으로 시스템을 확장할 수 있도록 유연함을 부여했습니다.
*   **게임 컨셉에 따른 체력(HP) 및 마나(MP)의 직관적 분리**:
    단순 텍스트 출력을 넘어 실제 게임 시스템의 자원 관리를 모사할 수 있도록 설계했습니다. 공격 행위는 기술 사용에 따른 피로도와 에너지를 나타내므로 **마나(MP)가 감소**하고, 외부 타격에 의한 방어 및 생존 상태는 **체력(HP)이 감소**하게 분리하여 상태 변화의 독립성을 보장했습니다.

### 2) 관리하는 데이터 및 핵심 속성
인터페이스를 구현하는 각 클래스는 상태를 안전하게 관리하기 위해 필드를 private으로 은닉(캡슐화)합니다.
*   `name` (String): 캐릭터의 개별 이름.
*   `hp` (int): 캐릭터의 생명력. 외부 피해(takeDamage)를 입을 때 감소하며, 최소값은 0으로 제한됩니다.
*   `mp` (int): 캐릭터의 행동력(마나). 공격(attack)할 때 소모되며, 최소값은 0으로 제한됩니다.

### 3) 설계 시 고려한 예외 및 안전 장치
*   체력(HP)이나 마나(MP)는 감산 연산 중 `0` 이하로 떨어질 위험이 있습니다.
*   이를 방지하기 위해 각 구현체는 내부 감산 로직에서 `Math.max(0, current - loss)` 방식을 적용하여 언더플로우를 사전에 차단하였습니다.

---

## 2. 🗂️ 인터페이스를 구현(implements)한 클래스의 설명

시스템의 구체적인 플레이어 캐릭터로 **전사(`Warrior`)**, **마법사(`Wizard`)**, **궁수(`Archer`)** 3가지 클래스를 정의했습니다. 각 클래스는 공통 속성을 은닉하여 관리하며, 약속된 모든 인터페이스의 행동을 오버라이딩하여 고유하게 재정의합니다.

### 1) 클래스의 내부 구성 속성 (멤버 변수)
모든 직업 클래스는 다음 3가지의 속성을 가지며, 정보 은닉(Information Hiding)을 위해 `private` 접근 제어자로 캡슐화되어 있습니다.
*   `name` (`String`): 캐릭터의 고유 이름을 저장합니다.
*   `hp` (`int`): 캐릭터의 생존에 관여하는 체력 수치입니다. 외부 타격 피해를 입었을 때 감소합니다.
*   `mp` (`int`): 캐릭터의 액션에 관여하는 마나 수치입니다. 자신의 일반 공격을 시도할 때 소모됩니다.

### 2) 클래스별 오버라이딩 메서드 요약 및 설명
각 클래스는 다중 구현(`implements PlayableCharacter, Movable, Attackable`)을 통해 다음과 같이 핵심 행동을 오버라이딩했습니다.

| 구현 클래스 | 구현하는 인터페이스 | 오버라이딩한 핵심 메서드 | 메서드 오버라이딩 주요 동작 |
| :--- | :--- | :--- | :--- |
| **`Warrior`** | `PlayableCharacter`, `Movable`, `Attackable` | `move()`<br>`attack()`<br>`useSkill()`<br>`takeDamage()` | 무거운 갑옷을 입고 묵직하게 이동합니다.<br>물리 근접 검 공격을 수행하며 **자신 MP 10 소모**합니다.<br>전사 시그니처 스킬인 "휠윈드"를 시전합니다.<br>피해량만큼 **자신 HP가 감소**합니다. |
| **`Wizard`** | `PlayableCharacter`, `Movable`, `Attackable` | `move()`<br>`attack()`<br>`useSkill()`<br>`takeDamage()` | 마법을 이용해 부드럽게 순간이동하며 이동합니다.<br>원거리 파이어볼 마법을 시전하며 **자신 MP 15 소모**합니다.<br>광역 마법인 "블리자드"를 시전합니다.<br>피해량만큼 **자신 HP가 감소**합니다. |
| **`Archer`** | `PlayableCharacter`, `Movable`, `Attackable` | `move()`<br>`attack()`<br>`useSkill()`<br>`takeDamage()` | 민첩한 발걸음으로 장애물을 뛰어넘으며 질주합니다.<br>정밀 바람의 화살을 사격하며 **자신 MP 8 소모**합니다.<br>광역 화살 세례인 "멀티플 샷"을 시전합니다.<br>피해량만큼 **자신 HP가 감소**합니다. |

---

## 3. 💻 코드와 코드 설명

### 1) 인터페이스 코드와 인터페이스 설명

#### 📝 인터페이스 소스 코드 (`src/PlayableCharacter.java`)
```java
// 이동 능력을 부여하는 인터페이스
interface Movable {
    // 캐릭터가 맵 상에서 움직이는 행동을 정의하는 추상 메서드
    void move();
}

// 전투 및 공격 능력을 부여하는 인터페이스
interface Attackable {
    // 캐릭터가 공격하는 행동을 정의하는 추상 메서드
    void attack();
}

// 플레이 가능한 캐릭터로서의 고유 기본 행동 및 상태 표준을 정의하는 인터페이스
interface PlayableCharacter {

    // 캐릭터의 고유 스킬을 사용하는 행동을 정의하는 추상 메서드
    void useSkill();

    // 캐릭터의 현재 상태 및 정보를 보여주는 행동을 정의하는 추상 메서드
    void showStatus();

    // 피해를 입었을 때 처리하는 행동을 정의하는 추상 메서드
    void takeDamage(int damage);

    // 캐릭터의 이름을 반환하는 추상 메서드
    String getName();
}
```

#### 💡 인터페이스 설명
*   **어떤 데이터를 관리하는가?**:
    인터페이스 자체는 상태 데이터(멤버 변수)를 가지지 않습니다. 오직 규약(메서드 원형)만을 선언하여, 구현체들이 이름(`getName`), 상태 출력(`showStatus`), 피해 연산(`takeDamage`)을 수행할 수 있도록 약속합니다. 데이터의 상태 관리는 전적으로 구체 클래스의 `private` 필드 몫으로 넘겨 독립성을 유지합니다.
*   **객체지향 설계 원칙 (SOLID) 적용 분석**:
    *   **인터페이스 분리 원칙 (ISP)**: 이동(`Movable`), 공격(`Attackable`), 캐릭터 관리(`PlayableCharacter`)가 서로 연관 없는 동작이므로 인터페이스를 완전히 분리하여 구현 클래스가 사용하지 않는 메서드에 의존하지 않도록 했습니다.
    *   **단일 책임 원칙 (SRP)**: 각각의 인터페이스는 오직 한 가지 종류의 책임(이동의 정의, 공격의 정의, 캐릭터 일반 정보 규정)에만 집중하도록 단일한 책임을 부여했습니다.
    *   **개방-폐쇄 원칙 (OCP)**: 새로운 캐릭터 직업군(예: 도적, 사제 등)을 추가할 때 기존 인터페이스나 핵심 동작 코드를 변경할 필요 없이 인터페이스만 새로 구현하면 되므로 확장에 열려 있고 수정에 닫혀 있습니다.
    *   **리스코프 치환 원칙 (LSP)**: `Movable`이나 `Attackable` 타입 참조 변수로 구체 인스턴스를 조작할 때, 부모 인터페이스의 논리적 계약을 위반하지 않고 안정적으로 대입하여 동작을 가동할 수 있습니다.

---

### 2) 인터페이스를 구현하는 클래스 코드와 설명

#### 📝 구현 클래스 소스 코드 (`src/Main.java` 상단부)
```java
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
```

#### 💡 구현 클래스 설명
*   **클래스의 역할**:
    각 클래스는 게임 내의 고유한 직업군 및 캐릭터 유닛을 정의합니다. 객체는 생성 시 이름, 체력(HP), 마나(MP) 상태를 가지며, 각 직업의 시각적 특징과 능력치 소모 패턴을 투영하여 서로 다른 방식으로 행동을 처리하도록 정의되었습니다.
*   **각 오버라이딩 메서드가 하는 구체적인 일**:
    *   `move()`: 각 직업군 고유의 기동 멘트를 콘솔에 출력합니다 (전사는 중장갑 이동, 마법사는 순간이동, 궁수는 민첩한 질주).
    *   `attack()`: 일반 공격 모션을 설명하고, 고유 소모 마나량(`Warrior: 10`, `Wizard: 15`, `Archer: 8`)만큼 자신의 마나 `mp`를 차감한 뒤 현재 마나를 출력합니다. 차감 후 마나가 `0` 미만으로 내려가지 않도록 안전장치를 가지고 있습니다.
    *   `useSkill()`: 각 직업의 강력한 스킬(휠윈드, 블리자드, 멀티플 샷) 사용을 출력합니다.
    *   `takeDamage(damage)`: 외부 공격 피해를 입었을 때, 피해량만큼 체력 `hp`를 감소시킵니다. 체력이 `0` 미만으로 떨어지지 않게 처리되어 있습니다.
    *   `getName()`: 캐릭터의 이름을 안전하게 반환하여, 외부 시스템에서 대상 캐릭터의 이름을 명시할 수 있도록 지원합니다.

---

### 3) Main 메서드 코드와 설명

#### 📝 Main 메서드 소스 코드 (`src/Main.java` 하단부)
```java
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
```

#### 💡 Main 메서드 흐름 설명
1.  **객체 생성 및 초기화**: `new` 연산자와 각 구현 클래스의 생성자를 이용하여 `Warrior(아라곤)`, `Wizard(간달프)`, `Archer(레골라스)` 객체를 힙 메모리에 인스턴스화하고 초깃값(체력, 마나)을 설정합니다. 이때 변수 타입을 인터페이스가 아닌 구체 클래스 타입으로 직접 선언하여, 강제 형변환(`Casting`) 없이 다중 구현된 모든 인터페이스의 메서드들을 직접 호출할 수 있도록 가독성을 확보했습니다.
2.  **초기 상태 확인**: 생성 직후 `showStatus()`를 통해 초기 체력과 마나가 잘 배정되었는지 확인합니다.
3.  **이동 규약 검증**: 각 인스턴스의 `move()`를 실행하여 직업별 독특한 이동 멘트가 발생하는지 시뮬레이션합니다.
4.  **고유 스킬 검증**: `useSkill()`을 가동하여 각 직업 고유의 개성 있는 액티브 스킬 사용 로그가 출력되는지 점검합니다.
5.  **공격 시 마나 차감 시뮬레이션**: `attack()`을 실행하여 공격 액션 로그와 동시에 내부 상태값인 마나(`mp`)가 약속된 수치만큼 정상적으로 감소하고 안전하게 적용되는지 테스트합니다.
6.  **외부 충격 및 체력 피해 시뮬레이션**: `takeDamage(damage)` 메서드를 직접 호출하여 특정 데미지가 부여되었을 때, 대상 캐릭터의 인스턴스 상태인 체력(`hp`)이 해당 값만큼 실시간 차감되고 변경된 상태가 출력되는지 검증합니다.
7.  **최종 상태 확인**: 모든 전투 행위가 수행된 뒤 `showStatus()`를 재호출하여, 감산된 체력과 마나 수치가 누적 반영된 최종 데이터를 최종 검증합니다.

---

### 4) Main 메서드 실행 결과 설명

#### 📝 콘솔 출력 결과
```text
=== 캐릭터 생성 및 초기 상태 ===
[이름: 아라곤 | 직업: 전사 | 체력(HP): 200 | 마나(MP): 150]
[이름: 간달프 | 직업: 마법사 | 체력(HP): 120 | 마나(MP): 100]
[이름: 레골라스 | 직업: 궁수 | 체력(HP): 140 | 마나(MP): 120]

=== 이동 행동 시뮬레이션 ===
아라곤(전사)이(가) 무거운 갑옷을 입고 묵직하게 걸어갑니다.
간달프(마법사)이(가) 부드럽게 순간이동하며 신속하게 이동합니다.
레골라스(궁수)이(가) 민첩한 발걸음으로 장애물을 뛰어넘으며 질주합니다.

=== 스킬 사용 시뮬레이션 ===
아라곤(전사)이(가) 휠윈드(Wheelwind) 스킬을 시전합니다!
간달프(마법사)이(가) 눈보라를 퍼붓는 블리자드(Blizzard) 마법을 시전합니다!
레골라스(궁수)이(가) 공중으로 수많은 화살을 퍼붓는 멀티플 샷(Multiple Shot)을 시전합니다!

=== 공격 시 마나 소모 시뮬레이션 ===
아라곤(전사)이(가) 검을 휘둘러 공격합니다! (자신의 MP 10 소모, 현재 MP: 140)
간달프(마법사)이(가) 강력한 파이어볼을 발사합니다! (자신의 MP 15 소모, 현재 MP: 85)
레골라스(궁수)이(가) 바람의 화살을 날립니다! (자신의 MP 8 소모, 현재 MP: 112)

=== 피해 발생 및 체력(HP) 감소 시뮬레이션 ===
[마법사 외부 피해 발생]
간달프이(가) 외부로부터 30만큼의 피해를 입었습니다. (현재 체력: 90)
[이름: 간달프 | 직업: 마법사 | 체력(HP): 90 | 마나(MP): 85]

[전사 외부 피해 발생]
아라곤이(가) 외부로부터 50만큼의 피해를 입었습니다. (현재 체력: 150)
[이름: 아라곤 | 직업: 전사 | 체력(HP): 150 | 마나(MP): 140]

=== 최종 상태 ===
[이름: 아라곤 | 직업: 전사 | 체력(HP): 150 | 마나(MP): 140]
[이름: 간달프 | 직업: 마법사 | 체력(HP): 90 | 마나(MP): 85]
[이름: 레골라스 | 직업: 궁수 | 체력(HP): 140 | 마나(MP): 112]
```

#### 💡 실행 결과 상세 분석
*   **다형적 출력과 기동 검증**:
    `move()`와 `useSkill()` 호출 시, 객체 타입에 맞는 오버라이딩 메서드가 동적으로 바인딩되어 각 직업군의 고유 멘트가 정상 출력되었습니다.
*   **자원 관리 검증 (MP 감소)**:
    공격(`attack()`)이 발동될 때, 각각 미리 정의된 마나 소모 규칙에 따라 값이 정상 차감되었습니다.
    *   **전사(아라곤)**: 초기 MP `150` ➡️ 공격 후 MP `140` (10 감소)
    *   **마법사(간달프)**: 초기 MP `100` ➡️ 공격 후 MP `85` (15 감소)
    *   **궁수(레골라스)**: 초기 MP `120` ➡️ 공격 후 MP `112` (8 감소)
*   **피해 연산 검증 (HP 감소)**:
    `takeDamage(damage)` 호출 시 객체 생명력인 `hp`가 즉시 감산 반영되었습니다.
    *   **마법사(간달프)**: 초기 HP `120` ➡️ 피해량 30 적용 후 HP `90` (30 감소)
    *   **전사(아라곤)**: 초기 HP `200` ➡️ 피해량 50 적용 후 HP `150` (50 감소)
    *   궁수(레골라스)는 피해 이력이 없어 최초 체력 `140`을 그대로 보존했습니다.
*   **최종 무결성 검증**:
    최종 상태 출력 시점의 HP와 MP 잔여 수치는 앞의 연산 시뮬레이션 결과 누적치와 정확하게 매칭되어, 메모리 상에서 객체의 인스턴스 정보가 성공적으로 영속/관리되고 있음을 입증합니다.
