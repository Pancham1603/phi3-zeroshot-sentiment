import React, { useState } from 'react';
import './App.css';
import ChatBox from './ChatBox';
import ChatForm from './ChatForm';
import Conversations from './Conversations'; 

function App() {
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]); 
  const [currentConversation, setCurrentConversation] = useState(null); 

  const addMessage = (text, sender) => {
    const date = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    const newMessage = { text, sender, date };
    setMessages([...messages, newMessage]);
    updateCurrentConversation([...messages, newMessage]);
  };

  const updateCurrentConversation = (updatedMessages) => {
    if (currentConversation !== null) {
      const updatedConversations = conversations.map((conv, index) =>
        index === currentConversation ? updatedMessages : conv
      );
      setConversations(updatedConversations);
    }
  };

  const handleSendMessage = async (userInput) => {
    addMessage(userInput, 'user');

    const response = await fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    addMessage(data.reply, 'bot');
  };

  const handleNewConversation = () => {
    if (currentConversation !== null) {
      setConversations([...conversations, messages]);
    }
    setMessages([]);
    setCurrentConversation(conversations.length);
  };

  const handleConversationClick = (index) => {
    setCurrentConversation(index);
    setMessages(conversations[index]);
  };

  return (
    <div className="app-container">
      <div className="conversations-container">
        <Conversations
          conversations={conversations}
          onConversationClick={handleConversationClick}
          onNewConversation={handleNewConversation}
        />
      </div>
      <div className="chat-container">
        <header className="chat-header">Chat with PHI-3</header>
        <ChatBox messages={messages} />
        <ChatForm onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}

export default App;
