// 당첨 상품 목록 및 상품 정보 표시
function PrizeList({
  wins,
  prizes,
  selectedPrize,
  onDelete,
  onShowDetail,
  onCloseDetail,
  onReset,
}) {
  // 상품별 획득 개수 계산 (같은 상품의 당첨 기록만 골라서 개수 세기)
  function countPrize(prizeId) {
    return wins.filter((win) => win.prize.id === prizeId).length;
  }

  return (
    <section className="prize-list">
      <div className="prize-header">
        <h2>획득한 선물 ({wins.length}개)</h2>
        <button className="btn-reset" onClick={onReset}>
          초기화
        </button>
      </div>

      {wins.length === 0 ? (
        <p className="empty">아직 획득한 선물이 없습니다.</p>
      ) : (
        <>
          {/* 상품별 획득 개수 */}
          <ul className="prize-summary" aria-label="상품별 획득 개수">
            {prizes.map((prize) => (
              <li key={prize.id}>
                <span>
                  {prize.emoji} {prize.name}
                </span>
                <strong>{countPrize(prize.id)}개</strong>
              </li>
            ))}
          </ul>

          {/* 당첨 순서 목록 */}
          <ol className="win-list" aria-label="당첨 순서 목록">
            {wins.map((win, index) => (
              <li
                key={win.recordId}
                onDoubleClick={() => onDelete(win.recordId)}
                onContextMenu={() => onShowDetail(win.prize)}
              >
                <span className="win-order">{index + 1}</span>
                <span className="win-emoji">{win.prize.emoji}</span>
                <span>{win.prize.name}</span>
              </li>
            ))}
          </ol>
        </>
      )}

      {/* 상품 상세 정보 */}
      {selectedPrize && (
        <div className="prize-detail">
          <h3>
            {selectedPrize.emoji} {selectedPrize.name}
          </h3>
          <p>{selectedPrize.description}</p>
          <p>상품 가치: {selectedPrize.value.toLocaleString()}원</p>
          <p>당첨 확률: {100 / prizes.length}%</p>
          <p>보유 개수: {countPrize(selectedPrize.id)}개</p>
          <button className="btn-close" onClick={onCloseDetail}>
            닫기
          </button>
        </div>
      )}
    </section>
  );
}

export default PrizeList;
