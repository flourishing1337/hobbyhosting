import { useRef, useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

export default function Showcase() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggleMusic = () => {
    const audio = audioRef.current;
    if (!audio) return;
    if (playing) {
      audio.pause();
    } else {
      audio.play();
    }
    setPlaying(!playing);
  };

  return (
    <div className="showcase-page">
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main>
        <section className="video-section">
          <h2>GP-Motor - Bilhandlare i Strängnäs.</h2>
          <video
            className="full-video"
            src="/videos/video1.mp4"
            autoPlay
            muted
            playsInline
            loop
          />
        </section>
        <section className="video-section">
          <h2>Olivträdgården - Olivträd av premium kvalité.</h2>
          <video
            className="full-video"
            src="/videos/video2.mp4"
            autoPlay
            muted
            playsInline
            loop
          />
        </section>
        <section className="video-section">
          <h2>Grekiska Tavernan - Restaurang i Strängnäs hamn.</h2>
          <video
            className="full-video"
            src="/videos/video3.mp4"
            autoPlay
            muted
            playsInline
            loop
          />
        </section>
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
      <button className="music-toggle" onClick={toggleMusic}>
        {playing ? "Music Off" : "Music On"}
      </button>
      <audio ref={audioRef} src="/music/theme.mp3" loop />
    </div>
  );
}
