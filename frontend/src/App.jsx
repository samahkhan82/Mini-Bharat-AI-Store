import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([
    { from: "system", text: "Welcome to Mini Bharat AI Store 👋" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = () => {
    if (!input.trim()) return;

    // Add user message
    const newMessage = { from: "user", text: input };
    setMessages([...messages, newMessage]);

    // Fake system reply
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { from: "system", text: "Got it! We'll process your request 🚀" },
      ]);
    }, 600);

    setInput("");
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", height: "100vh" }}>
      <header
        style={{
          background: "#128C7E",
          color: "white",
          padding: "10px",
          fontWeight: "bold",
        }}
      >
        Mini Bharat AI Store
      </header>

      <div
        style={{
          flex: 1,
          height: "calc(100% - 120px)",
          overflowY: "auto",
          padding: "10px",
          background: "#ECE5DD",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              margin: "5px 0",
              textAlign: msg.from === "user" ? "right" : "left",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: "10px",
                background:
                  msg.from === "user" ? "#DCF8C6" : "white",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <footer
        style={{
          padding: "10px",
          background: "#f0f0f0",
          display: "flex",
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{
            flex: 1,
            padding: "8px",
            borderRadius: "20px",
            border: "1px solid #ccc",
          }}
          placeholder="Type a message"
        />
        <button
          onClick={sendMessage}
          style={{
            marginLeft: "10px",
            padding: "8px 16px",
            borderRadius: "20px",
            border: "none",
            background: "#128C7E",
            color: "white",
            cursor: "pointer",
          }}
        >
          Send
        </button>
      </footer>
    </div>
  );
}

export default App;
