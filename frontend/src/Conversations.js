import React from 'react';
import './Conversations.css';

const Conversations = ({ conversations, onConversationClick, onNewConversation }) => {
  return (
    <div className="conversations-list">
      <button 
        className="New-Conversation-button" 
        onClick={onNewConversation}
      >
        New Conversation
      </button>
      {conversations.map((conv, index) => (
        <div
          key={index}
          className="conversation-item"
          onClick={() => onConversationClick(index)}
        >
          Conversation {index + 1}
        </div>
      ))}
    </div>
  );
};

export default Conversations;
