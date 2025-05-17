import Link from 'next/link';
import '../styles/globals.css';

export default function Home() {
  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main className="container">
        <h2>Welcome to HobbyHosting</h2>
        <p>Your home for simple app hosting.</p>
        <nav>
          <Link href="/login"><button>Login</button></Link>
          <Link href="/register"><button>Register</button></Link>
        </nav>
      </main>
    </div>
  );
}
