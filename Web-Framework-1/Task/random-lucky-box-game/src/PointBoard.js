// 닉네임과 보유 포인트 표시
function PointBoard({ nickname, onNicknameChange, points, openCount }) {
  return (
    <section className="point-board">
      <label className="nickname">
        <span>👤 닉네임</span>
        <input
          type="text"
          value={nickname}
          onChange={onNicknameChange}
          placeholder="이름 입력"
        />
      </label>

      <div className="stats">
        <div className="stat">
          <span className="stat-label">💰 보유 포인트</span>
          <strong className="stat-value">{points.toLocaleString()}P</strong>
        </div>
        <div className="stat">
          <span className="stat-label">📦 박스 이용 횟수</span>
          <strong className="stat-value">{openCount}회</strong>
        </div>
      </div>
    </section>
  );
}

export default PointBoard;
