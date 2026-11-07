import { useState, useEffect } from "react";
import "./App.css";
import PointBoard from "./PointBoard";
import { START_POINTS } from "./prizes";

function App() {
  // State 선언
  const [nickname, setNickname] = useState("");
  const [points, setPoints] = useState(START_POINTS);
  const [openCount, setOpenCount] = useState(0);

  // 포인트가 변경되면 브라우저 탭 제목 변경
  useEffect(() => {
    document.title = `럭키박스 | ${points.toLocaleString()}P`;
  }, [points]);

  // 닉네임 입력
  function changeNickname(e) {
    setNickname(e.target.value);
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
    </div>
  );
}

export default App;
