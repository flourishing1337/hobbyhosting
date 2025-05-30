import Link from "next/link";
import { useRef, useState } from "react";
import "../styles/globals.css";

export default function Showcase() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [playing, setPlaying] = useState(false);

  const toggleMusic = () => {
    if (audioRef.current) {
      if (playing) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setPlaying(!playing);
    }
  };

  return (
    <div className="showcase-container">
      <iframe
        className="showcase-video"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1&mute=1"
        title="Showcase video"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
      <button
        className="music-toggle"
        aria-label={playing ? "Turn music off" : "Turn music on"}
        onClick={toggleMusic}
      >
        {playing ? "🔊" : "🔈"}
      </button>
      <audio ref={audioRef} src="/music/theme.mp3" loop />
      <nav className="showcase-nav">
        <Link href="/">Home</Link>
      </nav>
    </div>
  );
}
