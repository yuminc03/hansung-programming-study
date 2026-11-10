import { DEFAULT_NICKNAME } from "./prizes";

// 닉네임과 보유 포인트 표시
function PointBoard({ nickname, onNicknameChange, points, openCount }) {
  // 닉네임을 입력하지 않으면(공백만 입력한 경우 포함) 기본 닉네임 표시
  const displayName = nickname.trim() === "" ? DEFAULT_NICKNAME : nickname;

  return (
    <section className="point-board">
      <label className="nickname">
        <span>닉네임</span>
        <input
          type="text"
          value={nickname}
          onChange={onNicknameChange}
          placeholder="이름 입력"
        />
      </label>

      {/* 보유 포인트와 박스 이용 횟수를 카드 형태로 크게 표시 */}
      <div className="stat-cards">
        <div className="stat-card point-card">
          <p className="stat-label">
            💰 <strong>{displayName}</strong>님의 보유 포인트
          </p>
          <p className="stat-value">{points.toLocaleString()}P</p>
        </div>

        <div className="stat-card count-card">
          <p className="stat-label">📦 박스 이용 횟수</p>
          <p className="stat-value">{openCount}회</p>
        </div>
      </div>
    </section>
  );
}

export default PointBoard;
