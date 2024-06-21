import React from 'react';
import './ChatBox.css';

const ChatBox = ({ messages }) => {
  return (
    <div className="chat-box">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.sender}`}>
          <div className="message-content">
            <p>{msg.text}</p>
            <span className="message-date">{msg.date}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatBox;
