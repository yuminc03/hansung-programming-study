import styled from "styled-components";

const Card = styled.div`
  background-color: #e8f5e9;
  border: 2px solid #4caf50;
  border-radius: 15px;
  padding: 20px;
  width: 220px;
  text-align: center;
`;

const Button = styled.button`
  background-color: #4caf50;
  color: #ffffff;
  padding: 10px;
  border: none;
  border-radius: 8px;
`;

function StyledCard() {
  return (
    <Card>
      <h2>🍵 녹차라떼</h2>
      <p>가격: 4,000원</p>
      <Button>주문하기</Button>
    </Card>
  );
}

export default StyledCard;
