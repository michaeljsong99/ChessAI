import React, {useState, useEffect }  from 'react';
import './App.css';
import WithMoveValidation from './WithMoveValidation';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <div style={boardsContainer}>
            <WithMoveValidation/>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;

const boardsContainer = {
  display: "flex",
  justifyContent: "space-around",
  alignItems: "center",
  flexWrap: "wrap",
  width: "100vw",
  marginTop: 30,
  marginBottom: 50
};