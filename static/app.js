// static/app.js
async function sendMessage(message) {
  const chat = document.getElementById("chat");
  // append user bubble
  const um = document.createElement("div");
  um.className = "message user";
  um.textContent = message;
  chat.appendChild(um);

  // add bot typing bubble
  const bm = document.createElement("div");
  bm.className = "message bot";
  bm.textContent = "Thinking...";
  chat.appendChild(bm);
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });
    const data = await res.json();
    bm.textContent = data.response || "No response.";
    chat.scrollTop = chat.scrollHeight;
  } catch (err) {
    bm.textContent = "Sorry — error contacting server. Check server logs.";
    console.error(err);
  }
}

document.getElementById("sendBtn").addEventListener("click", () => {
  const input = document.getElementById("input");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  sendMessage(text);
});
document.getElementById("input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") document.getElementById("sendBtn").click();
});
