import { render, screen, fireEvent, within } from "@testing-library/react";
import App from "./App";
import { DEFAULT_NICKNAME, RESET_NICKNAME } from "./prizes";

// 버튼과 목록 찾기
function getOpenButton() {
  return screen.getByRole("button", { name: /럭키박스 열기/ });
}

function getWinItems() {
  const list = screen.getByRole("list", { name: "당첨 순서 목록" });
  return within(list).getAllByRole("listitem");
}

// Math.random 결과를 순서대로 고정 (0 → 초콜릿, 0.3 → 곰인형, 0.6 → 이어폰, 0.9 → 영화관람권)
function mockRandom(...values) {
  const spy = jest.spyOn(Math, "random");
  values.forEach((value) => spy.mockReturnValueOnce(value));
}

afterEach(() => {
  jest.restoreAllMocks();
});

test("처음에는 1,000P이고 당첨 상품이 없다", () => {
  render(<App />);

  expect(screen.getByText("1,000P")).toBeInTheDocument();
  expect(screen.getByText("0회")).toBeInTheDocument();
  expect(screen.getByPlaceholderText("이름 입력")).toHaveValue(DEFAULT_NICKNAME);
  expect(screen.getByText("아직 당첨된 상품이 없습니다.")).toBeInTheDocument();
});

test("박스를 열면 200P가 차감되고 당첨 상품이 목록에 추가된다", () => {
  mockRandom(0);
  render(<App />);

  fireEvent.click(getOpenButton());

  expect(screen.getByText("800P")).toBeInTheDocument();
  expect(screen.getByText("1회")).toBeInTheDocument();
  expect(screen.getByText(/초콜릿 당첨!/)).toBeInTheDocument();
  expect(getWinItems()).toHaveLength(1);
});

test("같은 상품이 반복 당첨되면 개수가 누적된다", () => {
  mockRandom(0, 0, 0.3);
  render(<App />);

  fireEvent.click(getOpenButton());
  fireEvent.click(getOpenButton());
  fireEvent.click(getOpenButton());

  const summary = screen.getByRole("list", { name: "상품별 획득 개수" });
  const items = within(summary).getAllByRole("listitem");
  expect(items[0]).toHaveTextContent("초콜릿2개");
  expect(items[1]).toHaveTextContent("곰인형1개");
  expect(getWinItems()).toHaveLength(3);
});

test("5번 열면 포인트가 부족해 더 이상 열 수 없다", () => {
  render(<App />);

  for (let i = 0; i < 5; i++) {
    fireEvent.click(getOpenButton());
  }

  expect(screen.getByText("0P")).toBeInTheDocument();
  expect(getOpenButton()).toBeDisabled();
  expect(screen.getByText(/포인트가 부족합니다/)).toBeInTheDocument();

  // 비활성화된 버튼은 눌러도 변화 없음
  fireEvent.click(getOpenButton());
  expect(getWinItems()).toHaveLength(5);
});

test("더블클릭하면 기록이 삭제되고 포인트는 반환되지 않는다", () => {
  mockRandom(0, 0.9);
  render(<App />);

  fireEvent.click(getOpenButton());
  fireEvent.click(getOpenButton());
  fireEvent.doubleClick(getWinItems()[0]);

  const items = getWinItems();
  expect(items).toHaveLength(1);
  expect(items[0]).toHaveTextContent("영화관람권");
  expect(screen.getByText("600P")).toBeInTheDocument();
});

test("우클릭하면 상품 상세 정보가 표시되고 닫을 수 있다", () => {
  mockRandom(0.6);
  render(<App />);

  fireEvent.click(getOpenButton());
  const event = fireEvent.contextMenu(getWinItems()[0]);

  // preventDefault로 브라우저 기본 메뉴를 막으면 false 반환
  expect(event).toBe(false);
  expect(screen.getByText("노이즈 캔슬링 무선 이어폰")).toBeInTheDocument();

  fireEvent.click(screen.getByRole("button", { name: "닫기" }));
  expect(
    screen.queryByText("노이즈 캔슬링 무선 이어폰")
  ).not.toBeInTheDocument();
});

test("초기화하면 닉네임은 '럭키학생', 포인트, 목록, 결과, 횟수가 모두 초기화된다", () => {
  render(<App />);

  const input = screen.getByPlaceholderText("이름 입력");
  fireEvent.change(input, { target: { value: "홍길동" } });
  fireEvent.click(getOpenButton());
  fireEvent.click(getOpenButton());
  fireEvent.contextMenu(getWinItems()[0]);

  fireEvent.click(screen.getByRole("button", { name: /초기화/ }));

  expect(input).toHaveValue(RESET_NICKNAME);
  expect(screen.getByText("1,000P")).toBeInTheDocument();
  expect(screen.getByText("0회")).toBeInTheDocument();
  expect(screen.getByText("아직 당첨된 상품이 없습니다.")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "닫기" })).not.toBeInTheDocument();
  expect(getOpenButton()).toBeEnabled();
});
