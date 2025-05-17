import React, { useEffect, useState } from "react";

interface Message {
  id: number;
  username: string;
  message: string;
  created_at: string;
}

export interface ChatProps {
  apiUrl: string;
  token: string;
}

export const Chat: React.FC<ChatProps> = ({ apiUrl, token }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    fetch(`${apiUrl}/chat/messages`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then(setMessages)
      .catch(console.error);
  }, [apiUrl, token]);

  const sendMessage = async () => {
    if (!input) return;
    const resp = await fetch(`${apiUrl}/chat/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message: input }),
    });
    if (resp.ok) {
      const msg = await resp.json();
      setMessages((prev) => [...prev, msg]);
      setInput("");
    }
  };

  return (
    <div className="border rounded p-2">
      <div className="h-48 overflow-y-auto mb-2">
        {messages.map((m) => (
          <div key={m.id}>
            <strong>{m.username}:</strong> {m.message}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border px-2 py-1 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button
          onClick={sendMessage}
          className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
};
