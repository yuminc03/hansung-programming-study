// 럭키박스 열기 및 당첨 결과 표시
function LuckyBox({ points, cost, lastResult, message, onOpen }) {
  // 포인트가 박스 비용보다 적으면 열 수 없음
  const canOpen = points >= cost;

  return (
    <section className="lucky-box">
      <div className={lastResult ? "box-display opened" : "box-display"}>
        {lastResult ? (
          <>
            <span className="result-emoji">{lastResult.emoji}</span>
            <strong className="result-name">{lastResult.name}</strong>
          </>
        ) : (
          <span className="result-emoji">🎁</span>
        )}
      </div>

      <button className="btn-open" onClick={onOpen} disabled={!canOpen}>
        🎁 럭키박스 열기 ({cost}P)
      </button>

      {/* 조건부 렌더링: 포인트 부족 안내 */}
      {!canOpen && (
        <p className="warning">
          ⚠️ 포인트가 부족합니다! 박스를 열려면 {cost}P 이상 필요합니다.
        </p>
      )}

      <p className="message">{message}</p>
    </section>
  );
}

export default LuckyBox;
