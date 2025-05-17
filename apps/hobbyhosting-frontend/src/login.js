async function login(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const resp = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await resp.json().catch(() => ({}));
  if (resp.ok && data.access_token) {
    localStorage.setItem('token', data.access_token);
    alert('Logged in');
  } else {
    alert(data.detail || 'Login failed');
  }
}

document.getElementById('login-form').addEventListener('submit', login);
