const form = document.getElementById("login-form");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  message.textContent = "";
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  try {
    const resp = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await safeJson(resp);
    if (!resp.ok || !data) {
      message.style.color = "red";
      message.textContent = (data && data.detail) || "Login failed";
      return;
    }
    if (data.access_token) {
      localStorage.setItem("access_token", data.access_token);
      message.style.color = "green";
      message.textContent = "Success! Redirecting...";
      setTimeout(() => {
        window.location.href = "welcome.html";
      }, 500);
    } else {
      message.style.color = "red";
      message.textContent = "Unexpected response";
    }
  } catch (err) {
    message.style.color = "red";
    message.textContent = "Network error";
  }
});

async function safeJson(resp) {
  try {
    return await resp.json();
  } catch {
    return null;
  }
}
