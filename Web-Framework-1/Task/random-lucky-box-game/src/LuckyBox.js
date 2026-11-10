// 럭키박스 열기 및 당첨 결과 표시
function LuckyBox({ points, cost, prizes, lastResult, message, onOpen }) {
  // 포인트가 박스 비용보다 적으면 열 수 없음
  const canOpen = points >= cost;

  // 상품을 당첨 확률이 낮은 순(오름차순)으로 정렬 (원본 배열은 바꾸지 않도록 복사 후 정렬)
  const sortedPrizes = [...prizes].sort((a, b) => a.chance - b.chance);

  return (
    <section className="lucky-box">
      {/* 당첨 전에는 선물 상자, 당첨 후에는 마지막 당첨 상품 표시 */}
      {lastResult ? (
        <>
          <div className="box-emoji opened">
            {lastResult.emoji}
          </div>
          <p className="box-caption">{lastResult.name}</p>
        </>
      ) : (
        <>
          <div className="box-emoji">🎁</div>
          <p className="box-caption">어떤 선물이 나올까요?</p>
        </>
      )}

      <p className="message">{message}</p>

      <button className="btn-open" onClick={onOpen} disabled={!canOpen}>
        🎁 럭키박스 열기 ({cost}P)
      </button>

      {/* 조건부 렌더링: 포인트 부족 안내 */}
      {!canOpen && (
        <p className="warning">
          ⚠️ 포인트가 부족합니다! 박스를 열려면 {cost}P 이상 필요합니다.
        </p>
      )}

      {/* 럭키박스에서 나올 수 있는 상품 4종과 당첨 확률 */}
      <div className="prize-lineup">
        <p className="lineup-title">이 상자에서 나올 수 있는 선물</p>
        <ul>
          {sortedPrizes.map((prize) => (
            <li key={prize.id}>
              <span className="lineup-emoji">{prize.emoji}</span>
              <span className="lineup-name">{prize.name}</span>
              <span className="lineup-chance">{prize.chance}%</span>
              <span className="lineup-reward">+{prize.reward}P</span>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default LuckyBox;
