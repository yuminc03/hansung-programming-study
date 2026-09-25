// =====================================================================
// 미스틱 운세 뽑기 - DOM 조작 + 이벤트 처리 실습
// =====================================================================

// 랜덤으로 뽑힐 운세 목록 (이모지 + 문구)
const fortunes = [
  { emoji: "🌙", text: "오늘은 잠깐 멈춰서 숨을 고르는 날이에요." },
  { emoji: "🌟", text: "작은 행운이 예상치 못한 곳에서 찾아옵니다." },
  { emoji: "🔥", text: "미루던 일을 시작하기 딱 좋은 타이밍이에요." },
  { emoji: "🌊", text: "감정의 파도가 크더라도, 곧 잔잔해질 거예요." },
  { emoji: "🍀", text: "누군가에게 먼저 연락해보세요. 좋은 소식이 있을 수도." },
  { emoji: "☕", text: "오늘은 카페인 한 잔의 여유가 필요한 날." },
  { emoji: "🌈", text: "힘든 일 뒤엔 반드시 좋은 순간이 옵니다." },
  { emoji: "🕯️", text: "조용한 시간 속에서 답을 찾게 될 거예요." },
];

// ---------------------------------------------------------------------
// 1. 자주 쓸 요소들을 미리 변수에 담아두기 (getElementById)
// ---------------------------------------------------------------------
const nameInput = document.getElementById("name-input");
const drawButton = document.getElementById("draw-button");
const fortuneList = document.getElementById("fortune-list");

// ---------------------------------------------------------------------
// 2. 운세 카드 하나를 만드는 함수
//    (createElement로 요소를 만들고, appendChild로 조립)
// ---------------------------------------------------------------------
function createFortuneCard(name) {
  // 배열에서 랜덤으로 운세 하나 뽑기
  const randomIndex = Math.floor(Math.random() * fortunes.length);
  const { emoji, text } = fortunes[randomIndex];

  // 이름을 넣은 문구 만들기 (이름이 없으면 "당신"으로 대체)
  const displayName = name.trim() === "" ? "당신" : name.trim();
  const message = `\({displayName}님,\){text}`;

  // li 태그 생성 (강의 예제와 동일한 구조: li > div > (내용, 버튼))
  const li = document.createElement("li");

  const card = document.createElement("div");
  card.className = "card"; // CSS의 .card 스타일 적용

  const emojiSpan = document.createElement("span");
  emojiSpan.className = "emoji";
  emojiSpan.textContent = emoji;

  const p = document.createElement("p");
  p.className = "text";
  p.textContent = message;

  const closeBtn = document.createElement("button");
  closeBtn.className = "close-btn";
  closeBtn.textContent = "X";

  // -----------------------------------------------------------------
  // 3. 이벤트 처리 ① : 카드의 닫기 버튼 클릭 -> 카드 삭제
  //    closest("li")로 "이 버튼을 감싸고 있는 li"를 정확히 찾음
  // -----------------------------------------------------------------
  closeBtn.addEventListener("click", (event) => {
    // 카드 전체 클릭 이벤트(아래 4번)까지 같이 실행되지 않도록 막음
    event.stopPropagation();

    const target = closeBtn.closest("li");
    fortuneList.removeChild(target);
    checkEmpty();
  });

  // -----------------------------------------------------------------
  // 4. 이벤트 처리 ② : 카드 자체를 클릭해도 삭제되게 하기
  // -----------------------------------------------------------------
  card.addEventListener("click", () => {
    fortuneList.removeChild(li);
    checkEmpty();
  });

  // -----------------------------------------------------------------
  // 5. 이벤트 처리 ③ : 마우스를 올리면(mouseenter) 반짝임 효과,
  //    벗어나면(mouseleave) 효과 제거
  //    -> classList.add / remove 로 CSS 클래스를 붙였다 뗐다 함
  // -----------------------------------------------------------------
  card.addEventListener("mouseenter", () => {
    card.classList.add("glow");
  });
  card.addEventListener("mouseleave", () => {
    card.classList.remove("glow");
  });

  // -----------------------------------------------------------------
  // 6. 조립: 안쪽 요소부터 바깥으로 appendChild
  // -----------------------------------------------------------------
  card.appendChild(emojiSpan);
  card.appendChild(p);
  card.appendChild(closeBtn);
  li.appendChild(card);

  return li;
}

// ---------------------------------------------------------------------
// 7. "뽑기" 동작을 처리하는 함수
// ---------------------------------------------------------------------
function onDraw() {
  const name = nameInput.value;
  const newCard = createFortuneCard(name);

  // 새 카드를 목록 맨 위에 추가 (appendChild 대신 prepend 사용)
  fortuneList.prepend(newCard);

  // 입력창 초기화는 하지 않음 (이름은 계속 유지되게)
  checkEmpty();
}

// 목록이 비었을 때 안내 문구 보여주기 (선택 기능)
function checkEmpty() {
  const existingEmpty = document.getElementById("empty-msg");
  if (fortuneList.children.length === 0) {
    if (!existingEmpty) {
      const emptyMsg = document.createElement("li");
      emptyMsg.id = "empty-msg";
      emptyMsg.className = "empty";
      emptyMsg.textContent = "아직 뽑은 운세가 없어요. 버튼을 눌러보세요 🥠";
      fortuneList.appendChild(emptyMsg);
    }
  } else if (existingEmpty) {
    fortuneList.removeChild(existingEmpty);
  }
}

// ---------------------------------------------------------------------
// 8. 이벤트 등록: 버튼 클릭 시 onDraw 실행
// ---------------------------------------------------------------------
drawButton.addEventListener("click", onDraw);

// ---------------------------------------------------------------------
// 9. 이벤트 처리 ④ : 키보드 이벤트
//    입력창에서 Enter 키를 누르면 버튼을 누른 것과 동일하게 동작
// ---------------------------------------------------------------------
nameInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    onDraw();
  }
});

// 페이지 처음 로딩 시 빈 목록 안내 문구 표시
checkEmpty();
