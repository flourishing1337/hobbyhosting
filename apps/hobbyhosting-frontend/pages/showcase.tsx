import Link from "next/link";
import "../styles/globals.css";

export default function Showcase() {
  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main className="container">
        <h2>Our Work</h2>
        <p>Check out some of our previous films below.</p>
        <div className="video-wrapper">
          <iframe
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="Showcase video"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
    </div>
  );
}
