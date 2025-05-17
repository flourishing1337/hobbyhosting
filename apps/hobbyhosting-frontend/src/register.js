async function register(event) {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const resp = await fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await resp.json().catch(() => ({}));
  if (resp.ok && data.id) {
    alert("User created");
  } else {
    alert(data.detail || "Registration failed");
  }
}

document.getElementById("register-form").addEventListener("submit", register);
