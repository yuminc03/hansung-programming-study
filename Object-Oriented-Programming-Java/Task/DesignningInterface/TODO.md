# 프로젝트 구현 예정 작업 목록 (TODO List)

- [ ] Warrior 클래스 구현하기 (PlayableCharacter, Movable, Attackable 인터페이스를 다중 구현(implements)하여 전사 캐릭터의 행동을 오버라이딩합니다.)
- [ ] Wizard 클래스 구현하기 (PlayableCharacter, Movable, Attackable 인터페이스를 다중 구현(implements)하여 마법사 캐릭터의 행동을 오버라이딩합니다.)
- [ ] Archer 클래스 구현하기 (PlayableCharacter, Movable, Attackable 인터페이스를 다중 구현(implements)하여 궁수 캐릭터의 행동을 오버라이딩합니다.)
- [ ] Main 클래스 연동 테스트 (각 캐릭터 인스턴스를 생성하고 attack() 및 move() 동작이 올바르게 다형성으로 실행되는지 확인합니다.)
- [ ] 신규 직업 추가 고려 (도적(Thief), 성직자(Priest) 등 새로운 직업군의 확장성을 고려하여 설계가 유지되는지 검증합니다.)

## 객체지향 설계를 위한 인터페이스 리팩토링 검토 사항

- [x] 독립 인터페이스 설계 반영 (인터페이스 간 상속 관계를 제거하고 Movable, Attackable, PlayableCharacter를 독립적인 인터페이스로 정의합니다.)
- [x] 다형성 상호작용 반영 검토 (단순 attack() 대신 attack(PlayableCharacter target)을 정의해 캐릭터 간 전투 상호작용을 모델링합니다.)
- [x] 기본 피해 처리 로직 검토 (takeDamage(int damage)를 제공하여 구현 클래스들의 공통 데미지 계산 중복을 어떻게 처리할지 검토합니다.)
- [x] 캐릭터 상태 접근 메서드 검토 (getName(), getHp(), setHp(int hp)를 규정해 각 직업 객체의 주요 속성 접근 방식을 표준화합니다.)
