import { useRef, useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

export default function Showcase() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggleMusic = () => {
    if (!audioRef.current) return;
    if (playing) {
      audioRef.current.pause();
      setPlaying(false);
    } else {
      audioRef.current.play();
      setPlaying(true);
    }
  };

  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main>
        <section className="video-section">
          <video
            src="/videos/gp-motor.mp4"
            autoPlay
            loop
            muted
            playsInline
          />
          <div className="caption">GP-Motor - Bilhandlare i Strängnäs.</div>
        </section>
        <section className="video-section">
          <video
            src="/videos/olivtradgarden.mp4"
            autoPlay
            loop
            muted
            playsInline
          />
          <div className="caption">Olivträdgården - Olivträd av premium kvalité.</div>
        </section>
        <section className="video-section">
          <video
            src="/videos/grekiska-tavernan.mp4"
            autoPlay
            loop
            muted
            playsInline
          />
          <div className="caption">Grekiska Tavernan - Restaurang i Strängnäs hamn.</div>
        </section>
        <button className="music-toggle" onClick={toggleMusic}>
          {playing ? "Mute" : "Music"}
        </button>
        <audio ref={audioRef} src="/music/theme.mp3" loop />
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
    </div>
  );
}
