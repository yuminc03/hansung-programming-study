// =====================================================================
// PointBoard.js : 닉네임 입력창과 보유 포인트, 박스 이용 횟수를 보여주는 자식 컴포넌트
// =====================================================================

// 닉네임을 입력하지 않았을 때 대신 보여줄 기본 닉네임 가져오기
import { DEFAULT_NICKNAME } from "./prizes";

// ---------------------------------------------------------------------
// PointBoard() : 닉네임과 보유 포인트를 화면에 표시하는 함수형 컴포넌트
// - 부모(App)에게 받은 Props를 매개변수 자리에서 바로 분할 대입으로 꺼내 씀
//   nickname        : 현재 닉네임 입력값
//   onNicknameChange: 닉네임 입력창에 글자를 입력할 때 실행할 함수 (App의 changeNickname)
//   points          : 현재 보유 포인트
//   openCount       : 박스 이용 횟수
// ---------------------------------------------------------------------
function PointBoard({ nickname, onNicknameChange, points, openCount }) {
  // displayName: 화면에 보여줄 닉네임
  // - 입력값의 앞뒤 공백을 지운 결과(trim)가 빈 문자열이면 기본 닉네임, 아니면 입력한 닉네임
  const displayName = nickname.trim() === "" ? DEFAULT_NICKNAME : nickname;

  // ----- 화면(JSX) 반환 -----
  return (
    // 닉네임·포인트 영역 전체 (연보라색 박스)
    <section className="point-board">
      {/* 닉네임 입력 줄: '닉네임' 글자와 입력창 */}
      <label className="nickname">
        <span>닉네임</span>
        {/* 닉네임 입력창
            - value: nickname State 값을 입력창에 보여줌
            - onChange: 글자를 입력할 때마다 부모의 changeNickname 함수 실행
            - placeholder: 입력창이 비어 있을 때 흐리게 보이는 안내 글자 */}
        <input
          type="text"
          value={nickname}
          onChange={onNicknameChange}
          placeholder="이름 입력"
        />
      </label>

      {/* 보유 포인트와 박스 이용 횟수를 카드 형태로 크게 표시 */}
      <div className="stat-cards">
        {/* 보유 포인트 카드 (넓은 카드) */}
        <div className="stat-card point-card">
          {/* 'OOO님의 보유 포인트' 제목 (닉네임은 굵게) */}
          <p className="stat-label">
            💰 <strong>{displayName}</strong>님의 보유 포인트
          </p>
          {/* 보유 포인트 숫자 (toLocaleString으로 1,000처럼 쉼표 표시) */}
          <p className="stat-value">{points.toLocaleString()}P</p>
        </div>

        {/* 박스 이용 횟수 카드 */}
        <div className="stat-card count-card">
          <p className="stat-label">📦 박스 이용 횟수</p>
          {/* 박스를 연 횟수 */}
          <p className="stat-value">{openCount}회</p>
        </div>
      </div>
    </section>
  );
}

// PointBoard 컴포넌트를 App.js에서 쓸 수 있도록 내보내기 (default export)
export default PointBoard;
