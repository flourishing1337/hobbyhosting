import Link from "next/link";
import Header from "../components/Header";
import "../styles/globals.css";

export default function Welcome() {
  return (
    <div>
      <Header />
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
