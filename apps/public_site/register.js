const form = document.getElementById("register-form");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  message.textContent = "";
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const autoLogin = document.getElementById("auto-login").checked;
  try {
    const resp = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });
    const data = await safeJson(resp);
    if (!resp.ok || !data) {
      message.style.color = "red";
      message.textContent = (data && data.detail) || "Registration failed";
      return;
    }
    message.style.color = "green";
    message.textContent = "Registration successful";
    if (autoLogin) {
      await login(username, password);
    }
  } catch (err) {
    message.style.color = "red";
    message.textContent = "Network error";
  }
});

async function login(username, password) {
  try {
    const resp = await fetch("http://localhost:8000/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await safeJson(resp);
    if (resp.ok && data && data.access_token) {
      localStorage.setItem("access_token", data.access_token);
      window.location.href = "welcome.html";
    } else {
      message.style.color = "red";
      message.textContent = (data && data.detail) || "Auto login failed";
    }
  } catch {
    message.style.color = "red";
    message.textContent = "Network error during auto login";
  }
}

async function safeJson(resp) {
  try {
    return await resp.json();
  } catch {
    return null;
  }
}
