import React from "react";

function TailwindCard() {
  return (
    <div className="bg-purple-100 border-2 border-purple-500 rounded-2xl p-5 w-[220px] text-center">
      <h2>🧋 버블티</h2>
      <p>가격: 5,500원</p>
      <button className="bg-purple-500 text-white p-2 rounded-lg">
        주문하기
      </button>
    </div>
  );
}

export default TailwindCard;
