import { useRef, useState } from "react";
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
    <div>
      <header>
        <h1>Showcase</h1>
      </header>
      <main>
        <button className="music-toggle" onClick={toggleMusic}>
          {playing ? "Mute" : "Music"}
        </button>
        <audio ref={audioRef} src="/music/theme.mp3" loop />
        <section className="video-section">
          <h2>GP-Motor - Bilhandlare i Strängnäs.</h2>
          <video autoPlay loop muted playsInline src="/videos/gp-motor.mp4" />
        </section>
        <section className="video-section">
          <h2>Olivträdgården - Olivträd av premium kvalité.</h2>
          <video
            autoPlay
            loop
            muted
            playsInline
            src="/videos/olivtradgarden.mp4"
          />
        </section>
        <section className="video-section">
          <h2>Grekiska Tavernan - Restaurang i Strängnäs hamn.</h2>
          <video
            autoPlay
            loop
            muted
            playsInline
            src="/videos/grekiska-tavernan.mp4"
          />
        </section>
      </main>
    </div>
  );
}
