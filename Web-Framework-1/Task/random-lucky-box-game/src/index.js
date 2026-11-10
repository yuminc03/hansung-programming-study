// =====================================================================
// index.js : 리액트 앱의 시작 파일
// - public/index.html의 <div id="root"></div> 안에 App 컴포넌트를 그려 줌
// =====================================================================

// 리액트 라이브러리 가져오기 (JSX를 사용하기 위해 필요)
import React from "react";
// 리액트 컴포넌트를 실제 브라우저 화면(DOM)에 그려 주는 ReactDOM 가져오기
import ReactDOM from "react-dom/client";
// 전체 페이지에 적용할 기본 CSS 파일 가져오기
import "./index.css";
// 게임 전체 화면을 담당하는 App 컴포넌트 가져오기 (App.js의 export default)
import App from "./App";

// root: index.html에서 id가 "root"인 <div>를 찾아 리액트가 화면을 그릴 영역으로 지정
const root = ReactDOM.createRoot(document.getElementById("root"));
// root 영역 안에 App 컴포넌트를 렌더링(화면에 표시)
root.render(<App />);
