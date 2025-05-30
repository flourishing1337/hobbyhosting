import { useRef, useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

const projects = [
  "GP-Motor - Bilhandlare i Strängnäs.",
  "Olivträdgården - Olivträd av premium kvalité.",
  "Grekiska Tavernan - Restaurang i Strängnäs hamn.",
];

export default function Showcase() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggleMusic = () => {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setPlaying(!playing);
  };

  return (
    <div>
      <header>
        <h1>Vårt Arbete</h1>
      </header>
      <main>
        {projects.map((title, idx) => (
          <section key={idx} className="video-section">
            <h2>{title}</h2>
            <div className="video-wrapper">
              <iframe
                src="https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1&background=1"
                allow="autoplay; fullscreen"
                allowFullScreen
                title={title}
              ></iframe>
            </div>
          </section>
        ))}
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
      <audio ref={audioRef} loop src="/music/theme.mp3" />
      <button onClick={toggleMusic} className="music-toggle">
        {playing ? "Turn off music" : "Play music"}
      </button>
    </div>
  );
}
