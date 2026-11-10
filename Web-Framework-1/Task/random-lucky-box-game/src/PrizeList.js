// =====================================================================
// PrizeList.js : 당첨 상품 목록과 상품 상세 정보, 초기화 버튼을 보여주는 자식 컴포넌트
// =====================================================================

// ---------------------------------------------------------------------
// PrizeList() : 당첨 상품 목록과 상세 정보를 화면에 표시하는 함수형 컴포넌트
// - 부모(App)에게 받은 Props를 매개변수 자리에서 바로 분할 대입으로 꺼내 씀
//   wins         : 당첨 기록 배열 ({ recordId, prize } 객체들, 당첨 순서대로)
//   prizes       : 상품 4종 배열 (상품별 개수를 보여줄 때 사용)
//   selectedPrize: 상세 정보를 보여줄 상품 (없으면 null)
//   onDelete     : 기록을 더블클릭했을 때 실행할 삭제 함수 (App의 deleteWin)
//   onShowDetail : 기록을 오른쪽 클릭했을 때 실행할 상세 정보 함수 (App의 showDetail)
//   onCloseDetail: 상세 정보의 '닫기' 버튼을 눌렀을 때 실행할 함수 (App의 closeDetail)
//   onReset      : '초기화' 버튼을 눌렀을 때 실행할 함수 (App의 resetGame)
// ---------------------------------------------------------------------
function PrizeList({
  wins,
  prizes,
  selectedPrize,
  onDelete,
  onShowDetail,
  onCloseDetail,
  onReset,
}) {
  // -------------------------------------------------------------------
  // countPrize(prizeId) : 특정 상품을 몇 개 획득했는지 세어서 돌려주는 함수
  // - prizeId: 개수를 셀 상품의 id
  // - filter로 같은 상품의 당첨 기록만 골라낸 뒤, 그 배열의 길이(length)가 획득 개수
  // -------------------------------------------------------------------
  function countPrize(prizeId) {
    return wins.filter((win) => win.prize.id === prizeId).length;
  }

  // ----- 화면(JSX) 반환 -----
  return (
    // 당첨 상품 목록 영역 전체
    <section className="prize-list">
      {/* 목록 제목 줄: 전체 획득 개수와 초기화 버튼 */}
      <div className="prize-header">
        {/* wins.length: 당첨 기록의 개수 = 획득한 선물 개수 */}
        <h2>획득한 선물 ({wins.length}개)</h2>
        {/* 초기화 버튼: 누르면 부모의 resetGame 함수 실행 */}
        <button className="btn-reset" onClick={onReset}>
          초기화
        </button>
      </div>

      {/* 삼항 연산자로 당첨 기록이 있는지에 따라 다른 화면 표시
          - 기록이 0개면: 안내 문구
          - 기록이 있으면: 상품별 개수 + 당첨 순서 목록 */}
      {wins.length === 0 ? (
        <p className="empty">아직 획득한 선물이 없습니다.</p>
      ) : (
        <>
          {/* 상품별 획득 개수: 상품 4종을 map으로 하나씩 꺼내 개수와 함께 표시 */}
          <ul className="prize-summary" aria-label="상품별 획득 개수">
            {prizes.map((prize) => (
              // key: 목록 항목을 구분하는 고유 값 (상품 id)
              <li key={prize.id}>
                {/* 상품 이모지와 이름 */}
                <span>
                  {prize.emoji} {prize.name}
                </span>
                {/* countPrize 함수로 계산한 획득 개수 */}
                <strong>{countPrize(prize.id)}개</strong>
              </li>
            ))}
          </ul>

          {/* 당첨 순서 목록: 당첨 기록을 map으로 하나씩 꺼내 순서대로 표시
              - win: 당첨 기록 하나, index: 배열 안에서의 순서(0부터 시작) */}
          <ol className="win-list" aria-label="당첨 순서 목록">
            {wins.map((win, index) => (
              // 당첨 기록 한 줄
              // - key: 기록 고유 번호(recordId) → 같은 상품이 여러 번 있어도 구분됨
              // - onDoubleClick: 더블클릭하면 이 기록의 번호로 삭제 함수 실행
              // - onContextMenu: 오른쪽 클릭하면 이 기록의 상품으로 상세 정보 함수 실행
              <li
                key={win.recordId}
                onDoubleClick={() => onDelete(win.recordId)}
                onContextMenu={() => onShowDetail(win.prize)}
              >
                {/* 당첨 순서 번호 (index는 0부터 시작하므로 1을 더함) */}
                <span className="win-order">{index + 1}</span>
                {/* 당첨 상품 이모지 */}
                <span className="win-emoji">{win.prize.emoji}</span>
                {/* 당첨 상품 이름 */}
                <span>{win.prize.name}</span>
              </li>
            ))}
          </ol>
        </>
      )}

      {/* 조건부 렌더링: 상세 정보를 볼 상품(selectedPrize)이 있을 때만 상세 정보 표시 */}
      {selectedPrize && (
        <div className="prize-detail">
          {/* 상품 이모지와 이름 */}
          <h3>
            {selectedPrize.emoji} {selectedPrize.name}
          </h3>
          {/* 상품 설명 */}
          <p>{selectedPrize.description}</p>
          {/* 상품 가치 (toLocaleString으로 15,000처럼 쉼표 표시) */}
          <p>상품 가치: {selectedPrize.value.toLocaleString()}원</p>
          {/* 당첨 확률 */}
          <p>당첨 확률: {selectedPrize.chance}%</p>
          {/* 당첨 시 지급 포인트 */}
          <p>당첨 포인트: +{selectedPrize.reward}P</p>
          {/* 이 상품을 현재 몇 개 가지고 있는지 */}
          <p>보유 개수: {countPrize(selectedPrize.id)}개</p>
          {/* 닫기 버튼: 누르면 부모의 closeDetail 함수 실행 */}
          <button className="btn-close" onClick={onCloseDetail}>
            닫기
          </button>
        </div>
      )}
    </section>
  );
}

// PrizeList 컴포넌트를 App.js에서 쓸 수 있도록 내보내기 (default export)
export default PrizeList;
