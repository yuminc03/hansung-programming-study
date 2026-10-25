import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // 전역 스타일 파일
import App from './App'; // 방금 작성한 App 컴포넌트 불러오기

// HTML 문서에서 id가 'root'인 요소를 찾아 리액트 앱을 렌더링할 루트(Root)로 지정
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <App />
);