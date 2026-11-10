// 게임 기본 설정
export const START_POINTS = 1000;
export const BOX_COST = 200;

// 닉네임: 시작할 때는 본인 성명, 초기화하면 '럭키학생'
export const DEFAULT_NICKNAME = "추유민";
export const RESET_NICKNAME = "럭키학생";

// 당첨 상품 4종
// chance: 당첨 확률(%), 4개를 더하면 100이 되어야 함 (비싼 상품일수록 낮게 설정)
export const PRIZES = [
  {
    id: "chocolate",
    name: "초콜릿",
    emoji: "🍫",
    description: "달콤한 프리미엄 초콜릿 세트",
    value: 15000,
    chance: 40,
  },
  {
    id: "teddy",
    name: "곰인형",
    emoji: "🧸",
    description: "포근한 대형 곰인형",
    value: 35000,
    chance: 20,
  },
  {
    id: "earphone",
    name: "무선 이어폰",
    emoji: "🎧",
    description: "노이즈 캔슬링 무선 이어폰",
    value: 120000,
    chance: 10,
  },
  {
    id: "movie",
    name: "영화관람권",
    emoji: "🎫",
    description: "영화관 2인 관람권",
    value: 28000,
    chance: 30,
  },
];
