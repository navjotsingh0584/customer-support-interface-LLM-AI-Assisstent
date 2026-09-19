import { useState, useEffect } from "react";

import Login from "./components/Login";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ChatInput from "./components/ChatInput";
import ChatMessage from "./components/ChatMessage";
import Thinking from "./components/Thinking";
import UploadedFiles from "./components/UploadedFiles";

import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const [messages, setMessages] = useState([]);

  const [thinking, setThinking] = useState(false);

  const [sessionId, setSessionId] = useState(crypto.randomUUID());

  const [sessions, setSessions] = useState([]);

  function handleLogin(t) {
    localStorage.setItem("token", t);
    setToken(t);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setMessages([]);
  }

  async function loadSessions() {
    if (!token) return;

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/sessions",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (res.ok) {
        const data = await res.json();
        setSessions(data);
      }
    } catch (error) {
      console.log("SESSION LOAD ERROR", error);
    }
  }

  useEffect(() => {
    loadSessions();
  }, [token]);

  function newChat() {
    setSessionId(crypto.randomUUID());

    setMessages([
      {
        role: "assistant",
        message: "New chat started. How can I help you?",
      },
    ]);
  }

  async function openSession(id) {
    setSessionId(id);

    const res = await fetch(
      `http://127.0.0.1:8000/api/sessions/${id}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (res.ok) {
      const data = await res.json();
      setMessages(data);
    }
  }

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <Sidebar
        sessions={sessions}
        newChat={newChat}
        openSession={openSession}
        deleteChat={() => {}}
        sessionId={sessionId}
      />

      <div className="chat-area">
        <Header logout={logout} />

        <UploadedFiles sessionId={sessionId} />

        <div className="messages">
          {messages.map((m, i) => (
            <ChatMessage
              key={i}
              role={m.role}
              message={m.message}
              vision_context={m.vision_context}
            />
          ))}

          {thinking && <Thinking />}
        </div>

        <ChatInput
          setMessages={setMessages}
          setThinking={setThinking}
          sessionId={sessionId}
          refreshSessions={loadSessions}
        />
      </div>
    </div>
  );
}

export default App;