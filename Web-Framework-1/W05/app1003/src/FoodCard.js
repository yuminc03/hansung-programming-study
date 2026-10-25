import React from "react";
import styles from "./FoodCard.module.css";

function FoodCard(props) {
  return (
    <div className={styles.card}>
      <div className={styles.emoji}>{props.emoji}</div>

      <h2 className={styles.name}>{props.name}</h2>
      <p className={styles.name}>가격: {props.price}원</p>

      {/* popular 값이 true이면 '⭐ 인기 메뉴'를 화면에 출력 */}
      {props.popular && <p className={styles.popularText}>⭐ 인기 메뉴</p>}

      {/* spicy 값이 true이면 '》 매운 메뉴'를 화면에 출력 */}
      {props.spicy && <p className={styles.spicyText}>🌶️ 매운 메뉴</p>}
    </div>
  );
}

export default FoodCard;
