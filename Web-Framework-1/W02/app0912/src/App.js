import React from 'react';
import "./App.css";

function App() {
  // 3. 학생들의 점수 데이터를 순수 배열 변수로 초기값 지정
  // - const: ES6+ 재할당이 필요 없는 상수를 선언할 때 사용
  const scores = [95, 88, 72, 60, 45, 100, 80];

  // 4. 점수(score)를 받아 등급(A, B, C, F)을 판단하는 화살표 함수 (ES6+)
  const getGrade = (score) => {
    if (score >= 90) return "A";
    if (score >= 80) return "B";
    if (score >= 70) return "C";
    return "F"; // 70점 미만은 F
  };

  return (
    <div className="container">
      <h1 className="header">📊 학생 성적 평가 결과표</h1>
      <p className="subtitle">
        자바스크립트 배열(scores)과 map() 메서드를 활용한 리액트 컴포넌트
      </p>

      {/* 5, 성적 카드 목록 출력 구역 */}
      <ul className="list">
        {/* 6. 배멸 메서드 map()을 활용한 동적 목록 렌더링
          - map(): 배열의 요소(score)와 인덱스(index)를 순회하며 JSX 문법으로 변환
        */}
        {scores.map((score, index) => {
          // 순회 중인 학생 점수의 등급 계산
          const grade = getGrade(score);

          return (
            /* 7. React 리스트 렌더링의 고유한 식별자 key 속성 (인덱스 활용) */
            <li key={index} className="list-item">
              {/* 학생 순번 (0번 인덱스 + 1 처리) */}
              <span className="student-num">학생 {index + 1}</span>

              {/* 학생 점수 출력 */}
              <span className="score-text">
                점수: <strong>{score}점</strong>
              </span>

              {/*
                8. ES6+ 템플릿 문자열(백틱 …)을 활용한 동적 클래스 지정
                - grade. tolowerCase(): 'A' -> 'a', 'F' -> 'f' 소문자 변환
                - 최종 적용 클래스 예시: "badge badge-a", "badge badge-f" 등급별 스타일을 다르게 주기 위해
              */}
              <span className={`badge badge-${grade.toLowerCase()}`}>
                등급: {grade}
              </span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default App; // 9. App 컴포넌트 내보내기
