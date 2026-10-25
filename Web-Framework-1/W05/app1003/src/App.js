import React from "react";
import FoodCard from "./FoodCard";

function App() {
  return (
    <div>
      <h1>🍽️ 오늘 뭐 먹지?</h1>

      <FoodCard emoji="🍕" name="피자" price={15000} popular={true} spicy={false} />

      <FoodCard emoji="🍜" name="매운 라면" price={7000} popular={false} spicy={true} />

      <FoodCard emoji="🍔" name="햄버거" price={9000} popular={true} spicy={false} />
    </div>
  );
}

export default App;
