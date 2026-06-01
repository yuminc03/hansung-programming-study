// 이동 능력을 부여하는 독립적인 인터페이스
interface Movable {
    // 캐릭터가 맵 상에서 움직이는 행동을 정의하는 추상 메서드
    void move();
}

// 전투 및 공격 능력을 부여하는 독립적인 인터페이스
interface Attackable {
    // 캐릭터가 적을 공격하는 행동을 정의하는 추상 메서드
    void attack();
}

// 플레이 가능한 캐릭터로서의 고유 기본 행동을 정의하는 독립적인 인터페이스
public interface PlayableCharacter {

    // 캐릭터의 고유 스킬을 사용하는 행동을 정의하는 추상 메서드
    void useSkill();

    // 캐릭터의 현재 상태 및 정보를 보여주는 행동을 정의하는 추상 메서드
    void showStatus();
}
