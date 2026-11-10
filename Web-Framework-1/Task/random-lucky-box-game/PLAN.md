# 랜덤 럭키박스 게임 — 개발 계획

React의 컴포넌트, Props, Hook, 이벤트를 사용해 럭키박스 게임을 만든다.
요구사항 출처: `../React 과제-럭키박스게임.pdf`

## 1. 요구사항 요약

| 구분 | 내용 |
| --- | --- |
| 게임 시작 | 기본 닉네임은 본인 성명('추유민')이고 입력창에서 바꿀 수 있다(placeholder "이름 입력"). 시작 포인트는 1,000P이고, 시작할 때 당첨 상품은 없다. |
| 럭키박스 열기 | 한 번에 200P를 쓴다. 상품 4종 중 하나가 무작위로 당첨된다(각 25%). 같은 상품이 여러 번 당첨될 수 있다. 결과를 보여주고 획득 목록에 추가한다. |
| 포인트/종료 | 정상적으로 열 때마다 200P를 차감한다. 200P 미만이면 박스를 열 수 없고 포인트 부족 안내를 보여준다. 최대 5회까지 열 수 있다. |
| 당첨 상품 관리 | 상품별 획득 개수와 당첨 순서 목록을 보여준다. 더블클릭하면 그 기록을 삭제하고, 우클릭하면 상세 정보를 보여준다. 기록을 삭제해도 포인트는 돌려주지 않는다. |
| 게임 초기화 | 닉네임('럭키학생'), 포인트(1,000P), 당첨 목록, 마지막 결과, 이용 횟수를 모두 초기화한다. |
| 추가 기능 | 범위에서 제외한다(기본 기능만 구현). |

> 닉네임 값은 `prizes.js`의 `DEFAULT_NICKNAME`(시작, '추유민')과 `RESET_NICKNAME`(초기화, '럭키학생')으로 관리한다. 입력창을 비우면 "이름 입력" placeholder가 보인다.

## 2. 당첨 상품 (각 25%)

| id | 상품 | 설명 |
| --- | --- | --- |
| chocolate | 🍫 초콜릿 | 달콤한 프리미엄 초콜릿 세트 |
| teddy | 🧸 곰인형 | 포근한 대형 곰인형 |
| earphone | 🎧 무선 이어폰 | 노이즈 캔슬링 무선 이어폰 |
| movie | 🎫 영화관람권 | 영화관 2인 관람권 |

## 3. 파일 및 컴포넌트 구조

```
src/
├── App.js         게임 전체 화면, 상태와 이벤트 핸들러 관리
├── LuckyBox.js    럭키박스 열기 버튼, 포인트 부족 안내, 당첨 결과 표시
├── PointBoard.js  닉네임 입력, 보유 포인트, 이용 횟수 표시
├── PrizeList.js   획득 개수 요약, 당첨 순서 목록, 상품 상세 정보
├── prizes.js      상수(시작 포인트, 박스 비용)와 상품 데이터
├── App.css        전체 화면 스타일 (직접 작성)
└── App.test.js    게임 동작 테스트
```

## 4. 상태 및 Props 설계

### App (상태 보관)

| 상태 | 초기값 | 설명 |
| --- | --- | --- |
| `nickname` | `DEFAULT_NICKNAME` | 닉네임 입력값 |
| `points` | `1000` | 보유 포인트 |
| `wins` | `[]` | `{ recordId, prizeId }` 배열, 당첨 순서대로 |
| `lastResult` | `null` | 마지막 당첨 상품 |
| `openCount` | `0` | 박스 이용 횟수 |
| `message` | 안내 문구 | 결과/경고 메시지 |
| `selectedPrize` | `null` | 우클릭으로 고른 상세보기 상품 |

- `recordId`: `useRef` 카운터로 만든다. 같은 상품이 여러 번 당첨돼도 기록마다 고유한 key를 갖게 하기 위해서다.
- `useEffect`: 포인트가 바뀌면 `document.title`을 갱신한다.

### 핸들러 → Props 흐름

| 핸들러 | 동작 | 전달 대상 |
| --- | --- | --- |
| `changeNickname(e)` | 닉네임 변경 | PointBoard `onNicknameChange` |
| `openBox()` | 포인트 확인 → 무작위 당첨 → 200P 차감, 목록 추가, 결과·횟수 갱신 | LuckyBox `onOpen` |
| `deleteWin(recordId)` | 해당 기록 삭제 (포인트는 그대로) | PrizeList `onDelete` |
| `showDetail(prize)` / `closeDetail()` | 상세 정보 열기/닫기 | PrizeList `onShowDetail` / `onCloseDetail` |
| `resetGame()` | 모든 상태 초기화 | PrizeList `onReset` (목록 제목 옆 초기화 버튼) |

## 5. 개발 단계

1. 브랜치 `feature/task-lucky-box-game` 생성, 스캐폴딩 커밋
2. PLAN.md / TODO.md / PROGRESS.md 작성
3. prizes.js + PointBoard + App 상태 골격
4. LuckyBox: 박스 열기, 포인트 차감, 포인트 부족 처리
5. PrizeList: 개수 요약, 순서 목록, 더블클릭 삭제, 우클릭 상세
6. 게임 초기화
7. App.css 스타일
8. App.test.js 동작 테스트
9. 최종 점검 (테스트, 빌드, 브라우저 확인), 문서 갱신

## 6. 검증 방법

- `npm test -- --watchAll=false`: 시작 상태, 1회 열기, 5회 후 비활성화와 부족 안내, 더블클릭 삭제, 우클릭 상세, 초기화
- `npm run build`: 경고 없이 빌드되는지 확인
- `npm start`: 브라우저에서 직접 동작 확인
