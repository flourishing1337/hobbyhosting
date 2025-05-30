import { useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [autoLogin, setAutoLogin] = useState(false);
  const [message, setMessage] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage("");
    try {
      const resp = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      const data = await resp.json().catch(() => null);
      if (!resp.ok || !data) {
        setMessage((data && data.detail) || "Registration failed");
        return;
      }
      if (autoLogin) {
        localStorage.setItem("access_token", data.access_token);
        window.location.href = "/welcome";
      } else {
        setMessage("Registration successful");
      }
    } catch {
      setMessage("Network error");
    }
  }

  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main className="container">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Username:
            <br />
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
          <label>
            Email:
            <br />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>
          <label>
            Password:
            <br />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
          <label>
            <input
              type="checkbox"
              checked={autoLogin}
              onChange={(e) => setAutoLogin(e.target.checked)}
            />{" "}
            Log in after registration
          </label>
          <button type="submit">Register</button>
        </form>
        {message && <p id="message">{message}</p>}
        <nav>
          <Link href="/">Home</Link>
          <Link href="/login">Login</Link>
        </nav>
      </main>
    </div>
  );
}
