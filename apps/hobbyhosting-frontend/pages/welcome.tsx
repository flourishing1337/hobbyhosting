import Link from "next/link";
import "../styles/globals.css";

export default function Welcome() {
  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main className="container">
        <h2>Welcome</h2>
        <p>You are logged in.</p>
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
    </div>
  );
}
