// 당첨 상품 목록 및 상품 정보 표시
function PrizeList({
  wins,
  prizes,
  selectedPrize,
  onDelete,
  onShowDetail,
  onCloseDetail,
}) {
  // 상품 id로 상품 정보 찾기
  function findPrize(prizeId) {
    return prizes.find((prize) => prize.id === prizeId);
  }

  // 상품별 획득 개수 계산
  const counts = wins.reduce((acc, win) => {
    acc[win.prizeId] = (acc[win.prizeId] || 0) + 1;
    return acc;
  }, {});

  // 우클릭: 브라우저 기본 메뉴 대신 상세 정보 표시
  function handleContextMenu(e, prize) {
    e.preventDefault();
    onShowDetail(prize);
  }

  return (
    <section className="prize-list">
      <h2>🏆 당첨 상품 ({wins.length}개)</h2>

      {/* 상품별 획득 개수 */}
      <ul className="prize-summary">
        {prizes.map((prize) => (
          <li key={prize.id}>
            <span>
              {prize.emoji} {prize.name}
            </span>
            <strong>{counts[prize.id] || 0}개</strong>
          </li>
        ))}
      </ul>

      {/* 당첨 순서 목록 */}
      {wins.length === 0 ? (
        <p className="empty">아직 당첨된 상품이 없습니다.</p>
      ) : (
        <>
          <p className="hint">🖱️ 더블클릭: 기록 삭제 / 우클릭: 상세 정보</p>
          <ol className="win-list">
            {wins.map((win, index) => {
              const prize = findPrize(win.prizeId);
              return (
                <li
                  key={win.recordId}
                  onDoubleClick={() => onDelete(win.recordId)}
                  onContextMenu={(e) => handleContextMenu(e, prize)}
                >
                  <span className="win-order">{index + 1}</span>
                  <span>
                    {prize.emoji} {prize.name}
                  </span>
                </li>
              );
            })}
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
          <p>보유 개수: {counts[selectedPrize.id] || 0}개</p>
          <button className="btn-close" onClick={onCloseDetail}>
            닫기
          </button>
        </div>
      )}
    </section>
  );
}

export default PrizeList;
