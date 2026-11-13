// =====================================================================
// App.js : 게임 전체 화면과 주요 기능을 관리하는 최상위(부모) 컴포넌트
// - 게임의 모든 상태(State)를 이곳에서 관리하고,
//   자식 컴포넌트(PointBoard, LuckyBox, PrizeList)에 Props로 값과 함수를 전달함
// =====================================================================

// 리액트 Hook 가져오기
// - useState: 컴포넌트가 기억하고 관리하는 값(State)을 만들 때 사용
// - useRef  : 값이 바뀌어도 화면을 다시 그리지 않는 로컬 변수를 만들 때 사용
import { useState, useRef } from "react";
// 게임 화면 전체에 적용할 CSS 파일 가져오기
import "./App.css";
// 닉네임과 보유 포인트를 보여주는 자식 컴포넌트 가져오기
import PointBoard from "./PointBoard";
// 럭키박스 열기 버튼과 당첨 결과를 보여주는 자식 컴포넌트 가져오기
import LuckyBox from "./LuckyBox";
// 당첨 상품 목록과 상품 상세 정보를 보여주는 자식 컴포넌트 가져오기
import PrizeList from "./PrizeList";
// prizes.js에서 게임 설정값과 상품 데이터 가져오기 (normal export → 중괄호로 가져옴)
import {
  START_POINTS, // 시작 포인트 (1000)
  BOX_COST, // 박스 1회 비용 (200)
  DEFAULT_NICKNAME, // 시작 닉네임 (본인 성명)
  RESET_NICKNAME, // 초기화 닉네임 ('럭키학생')
  PRIZES, // 당첨 상품 4종 배열
} from "./prizes";

// START_MESSAGE: 게임 시작/초기화 때 보여줄 안내 메시지
const START_MESSAGE = "럭키박스를 열어 행운을 확인하세요!";

// ---------------------------------------------------------------------
// pickPrize() : 상품별 당첨 확률(chance)에 따라 상품 하나를 뽑아서 돌려주는 함수
// - 0~100 사이 난수를 만들고, 확률을 앞에서부터 더해 가다가 난수보다 커지는 상품이 당첨
// - 예) 초콜릿 40, 곰인형 20 → 난수 0~40 미만: 초콜릿, 40~60 미만: 곰인형
// - State를 사용하지 않으므로 App 컴포넌트 바깥에 일반 함수로 작성
// ---------------------------------------------------------------------
function pickPrize() {
  // random: 0 이상 100 미만의 무작위 소수 (Math.random()은 0~1 사이 값을 만듦)
  const random = Math.random() * 100;
  // sum: 앞에서부터 더한 확률의 합계 (처음에는 0)
  let sum = 0;

  // 상품 배열을 처음부터 끝까지 하나씩 확인 (i: 현재 확인 중인 상품의 번호)
  for (let i = 0; i < PRIZES.length; i++) {
    // 현재 상품의 확률을 합계에 더함 (예: 40 → 60 → 70 → 100)
    sum += PRIZES[i].chance;
    // 난수가 지금까지의 합계보다 작으면 이 상품이 당첨
    if (random < sum) {
      // 당첨된 상품 객체를 돌려주고 함수 종료
      return PRIZES[i];
    }
  }

  // 확률 합계가 100보다 작게 설정된 경우를 대비해 마지막 상품 반환
  return PRIZES[PRIZES.length - 1];
}

// ---------------------------------------------------------------------
// App() : 게임 전체를 담당하는 함수형 컴포넌트
// ---------------------------------------------------------------------
function App() {
  // ----- State 선언 (값이 바뀌면 화면이 다시 그려짐) -----
  // nickname: 닉네임 입력창에 들어 있는 값 / setNickname: nickname을 바꾸는 함수
  const [nickname, setNickname] = useState(DEFAULT_NICKNAME);
  // points: 현재 보유 포인트 / setPoints: points를 바꾸는 함수
  const [points, setPoints] = useState(START_POINTS);
  // wins: 당첨 기록 배열 (당첨 순서대로 { recordId, prize } 객체가 쌓임) / setWins: wins를 바꾸는 함수
  const [wins, setWins] = useState([]);
  // lastResult: 마지막으로 당첨된 상품 (아직 없으면 null) / setLastResult: lastResult를 바꾸는 함수
  const [lastResult, setLastResult] = useState(null);
  // openCount: 박스를 연 횟수 / setOpenCount: openCount를 바꾸는 함수
  const [openCount, setOpenCount] = useState(0);
  // message: 박스 영역에 보여줄 안내/결과 메시지 / setMessage: message를 바꾸는 함수
  const [message, setMessage] = useState(START_MESSAGE);
  // selectedPrize: 오른쪽 클릭으로 고른 상세 정보 상품 (없으면 null) / setSelectedPrize: 바꾸는 함수
  const [selectedPrize, setSelectedPrize] = useState(null);

  // nextRecordId: 다음 당첨 기록에 붙일 고유 번호 (1부터 시작)
  // - 같은 상품이 여러 번 당첨돼도 기록마다 번호가 달라서 구분 가능 (목록의 key로 사용)
  // - useRef 값(nextRecordId.current)은 바뀌어도 화면을 다시 그리지 않음
  const nextRecordId = useRef(1);

  // -------------------------------------------------------------------
  // changeNickname(e) : 닉네임 입력창에 글자를 입력할 때마다 실행되는 함수
  // - e: 입력 이벤트 객체, e.target.value: 입력창에 현재 들어 있는 글자
  // -------------------------------------------------------------------
  function changeNickname(e) {
    // 입력창의 값을 nickname State에 저장 → 화면의 닉네임도 함께 바뀜
    setNickname(e.target.value);
  }

  // -------------------------------------------------------------------
  // openBox() : '럭키박스 열기' 버튼을 눌렀을 때 실행되는 함수
  // - 포인트 확인 → 상품 뽑기 → 포인트 계산 → 당첨 기록 추가 → 결과 표시
  // -------------------------------------------------------------------
  function openBox() {
    // 보유 포인트가 박스 비용(200P)보다 적으면
    if (points < BOX_COST) {
      // 포인트 부족 메시지를 보여주고
      setMessage("❌ 포인트가 부족하여 박스를 열 수 없습니다!");
      // 함수를 바로 끝냄 (아래 코드는 실행되지 않음)
      return;
    }

    // prize: 상품별 당첨 확률에 따라 뽑은 당첨 상품 객체
    const prize = pickPrize();
    // record: 이번 당첨 기록 (recordId: 기록 고유 번호, prize: 당첨 상품 객체)
    const record = { recordId: nextRecordId.current, prize: prize };
    // 다음 기록에 쓸 번호를 1 증가
    nextRecordId.current += 1;

    // 박스 비용(200P)을 빼고, 당첨된 상품의 포인트(reward)를 더함
    setPoints((prev) => prev - BOX_COST + prize.reward);
    // 기존 당첨 기록 배열을 펼치고(...) 맨 뒤에 이번 기록을 추가한 새 배열로 바꿈
    setWins((prev) => [...prev, record]);
    // 마지막 당첨 결과를 이번 상품으로 바꿈
    setLastResult(prize);
    // 박스 이용 횟수를 1 증가
    setOpenCount((prev) => prev + 1);
    // 당첨 결과 메시지 표시 (템플릿 문자열로 상품 이모지, 이름, 지급 포인트를 넣음)
    setMessage(
      `🎉 축하합니다! ${prize.emoji} ${prize.name} 당첨! (+${prize.reward}P 적립)`
    );
  }

  // -------------------------------------------------------------------
  // deleteWin(recordId) : 당첨 기록을 더블클릭했을 때 그 기록을 삭제하는 함수
  // - recordId: 삭제할 당첨 기록의 고유 번호
  // - 사용한 포인트와 받은 포인트는 그대로 둠 (포인트 반환 없음)
  // -------------------------------------------------------------------
  function deleteWin(recordId) {
    // filter로 삭제할 번호와 다른 기록만 남긴 새 배열로 바꿈 (= 해당 기록만 삭제)
    setWins((prev) => prev.filter((win) => win.recordId !== recordId));
    // 삭제 안내 메시지 표시
    setMessage("🗑️ 당첨 기록을 삭제했습니다. (사용한 포인트는 반환되지 않습니다)");
  }

  // -------------------------------------------------------------------
  // showDetail(prize) : 당첨 기록을 오른쪽 클릭했을 때 상품 상세 정보를 여는 함수
  // - prize: 상세 정보를 보여줄 상품 객체
  // -------------------------------------------------------------------
  function showDetail(prize) {
    // 상세 정보로 보여줄 상품을 저장 → PrizeList에 상세 정보 영역이 나타남
    setSelectedPrize(prize);
  }

  // -------------------------------------------------------------------
  // closeDetail() : 상세 정보의 '닫기' 버튼을 눌렀을 때 상세 정보를 닫는 함수
  // -------------------------------------------------------------------
  function closeDetail() {
    // 선택된 상품을 null로 바꿈 → 상세 정보 영역이 사라짐
    setSelectedPrize(null);
  }

  // -------------------------------------------------------------------
  // resetGame() : '초기화' 버튼을 눌렀을 때 게임을 처음 상태로 되돌리는 함수
  // -------------------------------------------------------------------
  function resetGame() {
    // 닉네임을 '럭키학생'으로 변경
    setNickname(RESET_NICKNAME);
    // 포인트를 1,000P로 복원
    setPoints(START_POINTS);
    // 당첨 상품 목록을 빈 배열로 비움
    setWins([]);
    // 마지막 당첨 결과를 없앰
    setLastResult(null);
    // 박스 이용 횟수를 0으로 되돌림
    setOpenCount(0);
    // 열려 있던 상세 정보를 닫음
    setSelectedPrize(null);
    // 안내 메시지를 처음 문구로 되돌림
    setMessage(START_MESSAGE);
  }

  // ----- 화면(JSX) 반환 -----
  return (
    // 게임 전체를 감싸는 흰색 카드 영역
    <div className="container">
      {/* 게임 제목과 부제목 */}
      <h1>🎁 랜덤 럭키박스 게임</h1>
      <p className="subtitle">상자를 열고 특별한 선물을 획득하세요!</p>

      {/* 닉네임·보유 포인트·박스 이용 횟수 영역
          - nickname: 현재 닉네임 / onNicknameChange: 입력할 때 실행할 함수
          - points: 보유 포인트 / openCount: 박스 이용 횟수 */}
      <PointBoard
        nickname={nickname}
        onNicknameChange={changeNickname}
        points={points}
        openCount={openCount}
      />

      {/* 럭키박스 영역
          - points: 보유 포인트(열 수 있는지 판단) / cost: 박스 비용
          - prizes: 나올 수 있는 상품 목록 / lastResult: 마지막 당첨 상품
          - message: 안내 메시지 / onOpen: 열기 버튼을 누를 때 실행할 함수 */}
      <LuckyBox
        points={points}
        cost={BOX_COST}
        prizes={PRIZES}
        lastResult={lastResult}
        message={message}
        onOpen={openBox}
      />

      {/* 당첨 상품 목록 영역
          - wins: 당첨 기록 / prizes: 상품 목록(개수 계산용) / selectedPrize: 상세 정보 상품
          - onDelete: 더블클릭 삭제 함수 / onShowDetail: 오른쪽 클릭 상세 함수
          - onCloseDetail: 상세 닫기 함수 / onReset: 초기화 함수 */}
      <PrizeList
        wins={wins}
        prizes={PRIZES}
        selectedPrize={selectedPrize}
        onDelete={deleteWin}
        onShowDetail={showDetail}
        onCloseDetail={closeDetail}
        onReset={resetGame}
      />

      {/* 마우스 조작 방법 안내 문구 */}
      <p className="hint">상품 더블클릭: 삭제 / 마우스 오른쪽 클릭: 상세 정보</p>
    </div>
  );
}

// App 컴포넌트를 다른 파일(index.js)에서 쓸 수 있도록 내보내기 (default export)
export default App;
