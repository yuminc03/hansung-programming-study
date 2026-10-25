import React from "react";
import InlineCard from "./InlineCard";
import CssCard from "./CssCard";

import "./App.css";

function App() {
  return (
    <div className="app">
      <h1>React 스타일 적용 방식 비교</h1>

      <div className="card-container">
        <InlineCard />
        <CssCard />
      </div>
    </div>
  );
}

export default App;
