import { useState, useEffect } from "react";
import "./App.css";

function App() {
  // 초콜릿 가격
  const price = 1500;

  // State 선언
  const [money, setMoney] = useState(5000);
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState("수량을 선택하세요!");

  // 총 구매 금액
  const totalPrice = price * count;

  // 잔액이 번경되면 브라우저 법 제목 변경
  useEffect(() => {
    document.title = `자판기 잔액: ${money}원`;
  }, [money]);

  // 수량 증가
  function increase() {
    setCount((prev) => prev + 1);
  }

  // 수량 감소 (0 미만 방지)
  function decrease() {
    setCount((prev) => Math.max(0, prev - 1));
  }

  // 수량 초기화
  function resetCount() {
    setCount(0);
  }

  // 구매 처리
  function buySnack() {
    if (count === 0) {
      setMessage("⚠️ 수량을 먼저 선택하세요!");
      return;
    }

    if (totalPrice > money) {
      setMessage("❌ 잔액이 부족합니다!");
      return;
    }

    setMoney((prev) => prev - totalPrice);
    setMessage(`✅ 초콜릿 ${count}개 구매 완료!`);
    setCount(0);
  }

  return (
    <div className="container">
      <h1>🍫 초콜릿 자판기</h1>

      <h2>💰 현재 잔액: {money.toLocaleString()}원</h2>
      <p>초콜릿 가격: {price.toLocaleString()}원</p>

      <h2>선택 수량: {count}개</h2>

      {/* 수량 조절 버든 */}
      <button className="btn-increase" onClick={increase}>
        ➕ 증가
      </button>

      <button className="btn-decrease" onClick={decrease}>
        ➖ 감소
      </button>

      <button className="btn-reset" onClick={resetCount}>
        🔄 초기화
      </button>

      {/* 구매 금액 */}
      <h3>💳 총 구매 금액: {totalPrice.toLocaleString()}원</h3>

      {/* 조건부 렌더링 */}
      {totalPrice > money && (
        <p className="warning">⚠️ 구매 금액이 잔액보다 많습니다!</p>
      )}

      {/* 구매 결과 메시지 */}
      <p className="message">{message}</p>

      <button className="btn-buy" onClick={buySnack}>
        🛍️ 구매하기
      </button>
    </div>
  );
}

export default App;
