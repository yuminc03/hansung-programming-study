import { useState, useEffect, useRef } from "react";
import "./App.css";
import PointBoard from "./PointBoard";
import LuckyBox from "./LuckyBox";
import PrizeList from "./PrizeList";
import { START_POINTS, BOX_COST, PRIZES } from "./prizes";

const START_MESSAGE = "럭키박스를 열어 상품을 받아보세요!";

function App() {
  // State 선언
  const [nickname, setNickname] = useState("");
  const [points, setPoints] = useState(START_POINTS);
  const [wins, setWins] = useState([]);
  const [lastResult, setLastResult] = useState(null);
  const [openCount, setOpenCount] = useState(0);
  const [message, setMessage] = useState(START_MESSAGE);
  const [selectedPrize, setSelectedPrize] = useState(null);

  // 당첨 기록마다 고유 번호 부여 (같은 상품이 여러 번 당첨돼도 구분)
  const nextRecordId = useRef(1);

  // 포인트가 변경되면 브라우저 탭 제목 변경
  useEffect(() => {
    document.title = `럭키박스 | ${points.toLocaleString()}P`;
  }, [points]);

  // 닉네임 입력
  function changeNickname(e) {
    setNickname(e.target.value);
  }

  // 럭키박스 열기
  function openBox() {
    if (points < BOX_COST) {
      setMessage("❌ 포인트가 부족하여 박스를 열 수 없습니다!");
      return;
    }

    // 상품 4종 중 하나를 무작위로 선택 (각 25%)
    const prize = PRIZES[Math.floor(Math.random() * PRIZES.length)];
    const record = { recordId: nextRecordId.current, prizeId: prize.id };
    nextRecordId.current += 1;

    setPoints((prev) => prev - BOX_COST);
    setWins((prev) => [...prev, record]);
    setLastResult(prize);
    setOpenCount((prev) => prev + 1);
    setMessage(`🎉 축하합니다! ${prize.emoji} ${prize.name} 당첨!`);
  }

  // 당첨 기록 삭제 (사용한 포인트는 반환하지 않음)
  function deleteWin(recordId) {
    setWins((prev) => prev.filter((win) => win.recordId !== recordId));
    setMessage("🗑️ 당첨 기록을 삭제했습니다. (사용한 포인트는 반환되지 않습니다)");
  }

  // 상품 상세 정보 열기 / 닫기
  function showDetail(prize) {
    setSelectedPrize(prize);
  }

  function closeDetail() {
    setSelectedPrize(null);
  }

  return (
    <div className="container">
      <h1>🎁 랜덤 럭키박스 게임</h1>

      <PointBoard
        nickname={nickname}
        onNicknameChange={changeNickname}
        points={points}
        openCount={openCount}
      />

      <LuckyBox
        points={points}
        cost={BOX_COST}
        lastResult={lastResult}
        message={message}
        onOpen={openBox}
      />

      <PrizeList
        wins={wins}
        prizes={PRIZES}
        selectedPrize={selectedPrize}
        onDelete={deleteWin}
        onShowDetail={showDetail}
        onCloseDetail={closeDetail}
      />
    </div>
  );
}

export default App;
