import styles from "./ModuleCard.module.css";

function ModuleCard() {
  return (
    <div className={styles.card}>
      <h2>🍓 딸기라떼</h2>
      <p>가격: 4,500원</p>
      <button className={styles.button}>주문하기</button>
    </div>
  );
}

export default ModuleCard;
