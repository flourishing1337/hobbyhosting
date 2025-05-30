import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Header from "../components/Header";
import "../styles/globals.css";

export default function Film() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (router.query.success) setMessage("Payment successful!");
    if (router.query.canceled) setMessage("Payment canceled.");
  }, [router.query]);

  async function handleCheckout() {
    setLoading(true);
    setMessage("");
    const resp = await fetch("/api/create-checkout-session", {
      method: "POST",
    });
    if (resp.ok) {
      const data = await resp.json();
      if (data.url) {
        window.location.href = data.url;
        return;
      }
    }
    setLoading(false);
    setMessage("Unable to start checkout");
  }

  return (
    <div>
      <Header />
      <main className="container">
        <h2>We film your business</h2>
        <p>Get a professional promo video for $500.</p>
        <button onClick={handleCheckout} disabled={loading}>
          {loading ? "Loading..." : "Buy Now"}
        </button>
        {message && <p id="message">{message}</p>}
        <nav>
          <a href="/">Home</a>
        </nav>
      </main>
    </div>
  );
}
