// =====================================================================
// prizes.js : 게임 설정값(상수)과 당첨 상품 데이터를 모아 둔 파일
// - export const 로 내보내서 다른 파일에서 import { 이름 } 으로 가져다 씀 (normal export)
// =====================================================================

// ----- 게임 기본 설정 -----

// START_POINTS: 게임을 시작하거나 초기화할 때의 보유 포인트 (1,000P)
export const START_POINTS = 1000;
// BOX_COST: 럭키박스를 한 번 열 때 사용하는 포인트 (200P)
export const BOX_COST = 200;

// ----- 닉네임 설정 -----

// DEFAULT_NICKNAME: 게임을 처음 시작할 때의 기본 닉네임 (본인 성명)
//                   닉네임 입력창을 비워 두었을 때도 이 이름을 대신 보여줌
export const DEFAULT_NICKNAME = "추유민";
// RESET_NICKNAME: '초기화' 버튼을 눌렀을 때 바뀌는 닉네임
export const RESET_NICKNAME = "럭키학생";

// ----- 당첨 상품 4종 -----
// PRIZES: 당첨될 수 있는 상품 목록 (객체 4개가 들어 있는 배열)
// 상품 객체의 속성 설명
//   id          : 상품을 구분하는 고유 이름 (목록을 그릴 때 key로 사용)
//   name        : 화면에 보여줄 상품 이름
//   emoji       : 화면에 보여줄 상품 이모지
//   description : 상세 정보에 보여줄 상품 설명
//   value       : 상품 가치(원), 상세 정보에 표시
//   chance      : 당첨 확률(%), 4개를 더하면 100이 되어야 함 (비싼 상품일수록 낮게 설정)
//   reward      : 당첨되면 지급하는 포인트 (희귀한 상품일수록 많이 지급)
export const PRIZES = [
  // 1번 상품: 초콜릿 (확률 40%, 당첨 시 50P 지급)
  {
    id: "chocolate",
    name: "초콜릿",
    emoji: "🍫",
    description: "달콤한 프리미엄 초콜릿 세트",
    value: 15000,
    chance: 40,
    reward: 50,
  },
  // 2번 상품: 곰인형 (확률 20%, 당첨 시 150P 지급)
  {
    id: "teddy",
    name: "곰인형",
    emoji: "🧸",
    description: "포근한 대형 곰인형",
    value: 35000,
    chance: 20,
    reward: 150,
  },
  // 3번 상품: 무선 이어폰 (확률 10%, 당첨 시 300P 지급) - 가장 희귀한 상품
  {
    id: "earphone",
    name: "무선 이어폰",
    emoji: "🎧",
    description: "노이즈 캔슬링 무선 이어폰",
    value: 120000,
    chance: 10,
    reward: 300,
  },
  // 4번 상품: 영화관람권 (확률 30%, 당첨 시 100P 지급)
  {
    id: "movie",
    name: "영화관람권",
    emoji: "🎫",
    description: "영화관 2인 관람권",
    value: 28000,
    chance: 30,
    reward: 100,
  },
];
