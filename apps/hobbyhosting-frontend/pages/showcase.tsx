import { useRef, useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

const videos = [
  {
    title: "GP-Motor - Bilhandlare i Strängnäs.",
    url: "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
  {
    title: "Olivträdgården - Olivträd av premium kvalité.",
    url: "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
  {
    title: "Grekiska Tavernan - Restaurang i Strängnäs hamn.",
    url: "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
];

export default function Showcase() {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [musicOn, setMusicOn] = useState(false);

  const toggleMusic = () => {
    if (!audioRef.current) return;
    if (musicOn) {
      audioRef.current.pause();
    } else {
      audioRef.current.play().catch(() => {});
    }
    setMusicOn(!musicOn);
  };

  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
      </header>
      <main>
        {videos.map((video) => (
          <section key={video.title} className="video-section">
            <h2>{video.title}</h2>
            <div className="video-wrapper">
              <iframe
                src={video.url}
                allow="autoplay; fullscreen"
                allowFullScreen
                title={video.title}
              />
            </div>
          </section>
        ))}
        <button className="music-toggle" onClick={toggleMusic}>
          {musicOn ? "Turn music off" : "Turn music on"}
        </button>
        <audio ref={audioRef} src="/music/theme.mp3" loop />
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </main>
    </div>
  );
}
