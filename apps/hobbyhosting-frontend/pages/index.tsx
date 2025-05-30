import Link from "next/link";
import Header from "../components/Header";
import "../styles/globals.css";

export default function Home() {
  return (
    <div>
      <Header />
      <main className="container">
        <h2>Welcome to HobbyHosting</h2>
        <p>Your home for simple app hosting.</p>
        <nav>
          <Link href="/login">
            <button>Login</button>
          </Link>
          <Link href="/register">
            <button>Register</button>
          </Link>
          <Link href="/showcase">
            <button>Showcase</button>
          </Link>
          <Link href="/film">
            <button>Film your business</button>
          </Link>
        </nav>
      </main>
    </div>
  );
}
