// 닉네임과 보유 포인트 표시
function PointBoard({ nickname, onNicknameChange, points, openCount }) {
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
          <strong>{nickname === "" ? "이름 없음" : nickname}</strong>님의 보유
          포인트: <strong>{points.toLocaleString()}P</strong>
        </p>
        <p className="open-count">
          박스 이용 횟수: <strong>{openCount}회</strong>
        </p>
      </div>
    </section>
  );
}

export default PointBoard;
