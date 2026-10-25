function InlineCard() {
  const cardStyle = {
    backgroundColor: "#e3f2fd",
    border: "2px solid #2196f3",
    borderRadius: "15px",
    padding: "20px",
    width: "220px",
    textAlign: "center",
  };

  return (
    <div style={cardStyle}>
      <h2>☕ 아메리카노</h2>
      <p>가격: 3,000원</p>
      <button
        style={{
          backgroundColor: "#2196f3",
          color: "#ffffff",
          padding: "10px",
          border: "none",
          borderRadius: "8px",
        }}
      >
        주문하기
      </button>
    </div>
  );
}

export default InlineCard;
