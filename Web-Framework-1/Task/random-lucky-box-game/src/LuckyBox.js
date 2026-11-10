// 럭키박스 열기 및 당첨 결과 표시
function LuckyBox({ points, cost, lastResult, message, onOpen }) {
  // 포인트가 박스 비용보다 적으면 열 수 없음
  const canOpen = points >= cost;

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
    </section>
  );
}

export default LuckyBox;
