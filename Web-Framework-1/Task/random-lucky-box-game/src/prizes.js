// 게임 기본 설정
export const START_POINTS = 1000;
export const BOX_COST = 200;

// 당첨 상품 4종 (각 25% 확률)
export const PRIZES = [
  {
    id: "chocolate",
    name: "초콜릿",
    emoji: "🍫",
    description: "달콤한 프리미엄 초콜릿 세트",
    value: 15000,
  },
  {
    id: "teddy",
    name: "곰인형",
    emoji: "🧸",
    description: "포근한 대형 곰인형",
    value: 35000,
  },
  {
    id: "earphone",
    name: "무선 이어폰",
    emoji: "🎧",
    description: "노이즈 캔슬링 무선 이어폰",
    value: 120000,
  },
  {
    id: "movie",
    name: "영화관람권",
    emoji: "🎫",
    description: "영화관 2인 관람권",
    value: 28000,
  },
];
