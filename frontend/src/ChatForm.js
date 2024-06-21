import React, { useState } from 'react';
import './ChatForm.css';

const ChatForm = ({ onSendMessage }) => {
  const [userInput, setUserInput] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!userInput.trim()) return;
    onSendMessage(userInput);
    setUserInput('');
  };

  return (
    <form className="chat-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Type a message"
        autoComplete="off"
      />
      <button type="submit">Send</button>
    </form>
  );
};

export default ChatForm;
