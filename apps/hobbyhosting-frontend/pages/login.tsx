import { useState } from 'react';
import Link from 'next/link';
import '../styles/globals.css';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setMessage('');
    try {
      const resp = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await resp.json().catch(() => null);
      if (!resp.ok || !data) {
        setMessage((data && data.detail) || 'Login failed');
        return;
      }
      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token);
        setMessage('Success! Redirecting...');
        setTimeout(() => {
          window.location.href = '/welcome';
        }, 500);
      } else {
        setMessage('Unexpected response');
      }
    } catch {
      setMessage('Network error');
    }
  }

  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main className="container">
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Username:<br />
            <input value={username} onChange={e => setUsername(e.target.value)} required />
          </label>
          <label>
            Password:<br />
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          </label>
          <button type="submit">Login</button>
        </form>
        {message && <p id="message">{message}</p>}
        <nav>
          <Link href="/">Home</Link>
          <Link href="/register">Register</Link>
        </nav>
      </main>
    </div>
  );
}
