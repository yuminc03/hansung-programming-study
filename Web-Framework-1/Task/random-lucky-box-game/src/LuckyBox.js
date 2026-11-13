// =====================================================================
// LuckyBox.js : 럭키박스 열기 버튼과 당첨 결과, 나올 수 있는 상품 목록을 보여주는 자식 컴포넌트
// =====================================================================

// ---------------------------------------------------------------------
// LuckyBox() : 럭키박스 열기와 당첨 결과를 화면에 표시하는 함수형 컴포넌트
// - 부모(App)에게 받은 Props를 매개변수 자리에서 바로 분할 대입으로 꺼내 씀
//   points    : 현재 보유 포인트 (박스를 열 수 있는지 판단할 때 사용)
//   cost      : 박스 1회 비용 (200P)
//   prizes    : 나올 수 있는 상품 4종 배열
//   lastResult: 마지막으로 당첨된 상품 (없으면 null)
//   message   : 안내/결과 메시지
//   onOpen    : '럭키박스 열기' 버튼을 누를 때 실행할 함수 (App의 openBox)
// ---------------------------------------------------------------------
function LuckyBox({ points, cost, prizes, lastResult, message, onOpen }) {
  // canOpen: 박스를 열 수 있는지 여부 (보유 포인트가 비용 이상이면 true, 부족하면 false)
  const canOpen = points >= cost;

  // sortedPrizes: 당첨 확률이 낮은 순(오름차순)으로 정렬한 상품 배열
  // - [...prizes]로 배열을 복사한 뒤 정렬해서 원본(prizes) 순서는 바꾸지 않음
  // - sort((a, b) => a.chance - b.chance): 확률이 작은 상품이 앞으로 오도록 정렬
  const sortedPrizes = [...prizes].sort((a, b) => a.chance - b.chance);

  // ----- 화면(JSX) 반환 -----
  return (
    // 럭키박스 영역 전체 (연분홍색 박스)
    <section className="lucky-box">
      {/* 삼항 연산자로 조건에 따라 다른 화면 표시
          - lastResult가 있으면(당첨 후): 마지막 당첨 상품의 이모지와 이름
          - lastResult가 없으면(당첨 전): 선물 상자와 안내 문구
          - <> </>(Fragment): 불필요한 태그 없이 여러 요소를 하나로 묶음 */}
      {lastResult ? (
        <>
          {/* 당첨 상품 이모지 (opened 클래스로 튀어나오는 애니메이션 적용) */}
          <div className="box-emoji opened">
            {lastResult.emoji}
          </div>
          {/* 당첨 상품 이름 */}
          <p className="box-caption">{lastResult.name}</p>
        </>
      ) : (
        <>
          {/* 아직 열기 전: 선물 상자 이모지 */}
          <div className="box-emoji">🎁</div>
          {/* 아직 열기 전: 안내 문구 */}
          <p className="box-caption">어떤 선물이 나올까요?</p>
        </>
      )}

      {/* 안내/결과 메시지 (부모에게 받은 message) */}
      <p className="message">{message}</p>

      {/* 럭키박스 열기 버튼
          - onClick: 누르면 부모의 openBox 함수 실행
          - disabled: 열 수 없으면(canOpen이 false) 버튼을 비활성화해서 누를 수 없게 함 */}
      <button className="btn-open" onClick={onOpen} disabled={!canOpen}>
        🎁 럭키박스 열기 ({cost}P)
      </button>

      {/* 조건부 렌더링: 열 수 없을 때(!canOpen이 true)만 포인트 부족 안내 표시 */}
      {!canOpen && (
        <p className="warning">
          ⚠️ 포인트가 부족합니다! 박스를 열려면 {cost}P 이상 필요합니다.
        </p>
      )}

      {/* 럭키박스에서 나올 수 있는 상품 4종과 당첨 확률, 당첨 포인트 */}
      <div className="prize-lineup">
        <p className="lineup-title">이 상자에서 나올 수 있는 선물</p>
        <ul>
          {/* map으로 정렬된 상품 배열을 하나씩 꺼내 상품 카드(<li>)로 변환
              - key: 리액트가 목록의 각 항목을 구분하는 고유 값 (상품 id 사용) */}
          {sortedPrizes.map((prize) => (
            <li key={prize.id}>
              {/* 상품 이모지 */}
              <span className="lineup-emoji">{prize.emoji}</span>
              {/* 상품 이름 */}
              <span className="lineup-name">{prize.name}</span>
              {/* 당첨 확률 */}
              <span className="lineup-chance">{prize.chance}%</span>
              {/* 당첨 시 지급 포인트 */}
              <span className="lineup-reward">+{prize.reward}P</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

// LuckyBox 컴포넌트를 App.js에서 쓸 수 있도록 내보내기 (default export)
export default LuckyBox;
