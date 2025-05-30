import { useRef, useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

const projects = [
  {
    title: "GP-Motor - Bilhandlare i Strängnäs.",
    embedUrl:
      "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
  {
    title: "Olivträdgården - Olivträd av premium kvalité.",
    embedUrl:
      "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
  {
    title: "Grekiska Tavernan - Restaurang i Strängnäs hamn.",
    embedUrl:
      "https://player.vimeo.com/video/1089182703?autoplay=1&muted=1&loop=1",
  },
];

export default function Showcase() {
  const [musicOn, setMusicOn] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const toggleMusic = () => {
    if (!audioRef.current) return;
    if (musicOn) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setMusicOn(!musicOn);
  };

  return (
    <div>
      <header>
        <h1>HobbyHosting</h1>
        <nav>
          <Link href="/">Home</Link>
        </nav>
      </header>
      {projects.map((project) => (
        <section key={project.title} className="video-section">
          <div className="video-text">{project.title}</div>
          {/* To use your own MP4 files, place them under /public/videos and swap
              this iframe for a <video> element */}
          <iframe
            src={project.embedUrl}
            allow="autoplay; fullscreen; picture-in-picture"
            allowFullScreen
          ></iframe>
        </section>
      ))}
      <button className="music-toggle" onClick={toggleMusic}>
        {musicOn ? "Turn music off" : "Turn music on"}
      </button>
      <audio ref={audioRef} src="/music/theme.mp3" loop />
    </div>
  );
}
