import Link from "next/link";
import "../styles/globals.css";

const links = [
  { href: "/", label: "Home" },
  { href: "/login", label: "Login" },
  { href: "/register", label: "Register" },
  { href: "/showcase", label: "Showcase" },
  { href: "/film", label: "Film" },
  { href: "/welcome", label: "Welcome" },
];

export default function Header() {
  return (
    <header>
      <h1>HobbyHosting</h1>
      <nav>
        {links.map(({ href, label }) => (
          <Link key={href} href={href}>
            {label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
