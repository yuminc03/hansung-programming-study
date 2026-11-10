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

      <div className="point-info">
        <p>
          <strong>{displayName}</strong>님의 보유 포인트: <strong>{points.toLocaleString()}P</strong>
        </p>
        <p className="open-count">
          박스 이용 횟수: <strong>{openCount}회</strong>
        </p>
      </div>
    </section>
  );
}

export default PointBoard;
