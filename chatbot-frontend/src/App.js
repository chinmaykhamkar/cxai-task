import React from 'react';
import Chatbot from './components/Chatbot/Chatbot';
import './App.css';
import logo from './assets/logo.png';
/* App.js*/

function App() {
  return (
    <div>
      <div className='navbar'>
        <div className="logo">
          <img style={{ width: '25%' }} src={logo} alt="logo" />
        </div>
        <div className='title'>CXAPP Chatbot</div>
        <div className="logo">
          
        </div>
      </div>
      <Chatbot />
    </div>
  );
}

export default App;
