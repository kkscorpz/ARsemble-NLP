// static/app.js (replace your existing file with this)
// Clean, single-file client for ARsemble AI chat + tappable recommendations

(() => {
  const API_ENDPOINT = "/chat";
  const chat = document.getElementById("chat");
  const input = document.getElementById("input");
  const sendBtn = document.getElementById("sendBtn");

  // Ensure a single recommendation container sits under the chat
  let recs = document.getElementById("recs");
  if (!recs) {
    recs = document.createElement("div");
    recs.id = "recs";
    recs.className = "recs";
    const chatParent = chat.parentNode;
    chatParent.insertBefore(recs, chat.nextSibling);
  }

  // Helpers to append chat bubbles
  function appendUserBubble(text) {
    const el = document.createElement("div");
    el.className = "message user";
    el.textContent = text;
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
    return el;
  }

  function appendBotBubble(textOrHtml) {
    const el = document.createElement("div");
    el.className = "message bot";
    // allow basic HTML by converting newlines to <br>
    el.innerHTML = (textOrHtml || "").toString().replace(/\n/g, "<br>");
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
    return el;
  }

  function clearRecommendations() {
    recs.innerHTML = "";
    recs.style.display = "none";
  }

  // Render a short list of recommendation chips (limit to 6)
  function renderRecommendations(list) {
    clearRecommendations();
    if (!Array.isArray(list) || list.length === 0) return;
    recs.style.display = "flex";
    recs.style.flexWrap = "wrap";
    recs.style.gap = "8px";
    recs.style.padding = "10px";

    // Show up to 6 chips, prefer unique texts
    const unique = [];
    for (const it of list) {
      const key = (it.action_query || it.text || "").trim();
      if (!key) continue;
      if (!unique.find(u => u.key === key)) unique.push({ key, item: it });
      if (unique.length >= 6) break;
    }

    unique.forEach(({ key, item }) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "rec-chip";
      btn.textContent = item.text || item.action_query || key;
      btn.title = item.action_query || item.text || "";
      // styling (kept inline so it still looks ok if CSS missing)
      btn.style.border = "none";
      btn.style.padding = "8px 12px";
      btn.style.borderRadius = "999px";
      btn.style.cursor = "pointer";
      btn.style.background = "#eef6ff";
      btn.style.fontWeight = "600";
      btn.style.boxShadow = "0 2px 6px rgba(16,24,40,0.04)";

      // clicking a chip should *directly* run that action (no filling input)
      btn.addEventListener("click", async (ev) => {
        ev.preventDefault();
        // Prevent repeated clicks while this chip is executing
        if (btn.disabled) return;
        const q = (item.action_query || item.text || key).trim();
        if (!q) return;

        // visual feedback
        btn.disabled = true;
        const prevText = btn.textContent;
        btn.textContent = "⏳ Thinking...";
        btn.style.opacity = "0.65";

        try {
          // Immediately show user bubble and send
          // We clear the visible input to keep UI consistent
          input.value = "";
          await sendMessage(q);
        } finally {
          btn.disabled = false;
          btn.textContent = prevText;
          btn.style.opacity = "1";
        }
      });

      recs.appendChild(btn);
    });
  }

  // backend caller: returns parsed JSON or { reply: text }
  async function callBackend(q) {
    const body = { message: q };
    const res = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    // read as text then try parse (server may return JSON string)
    const text = await res.text();
    try {
      return JSON.parse(text);
    } catch (err) {
      // fallback: return plain text as reply
      return { reply: text };
    }
  }

  // Single-request guard (prevents duplicate concurrent calls)
  let requestInProgress = false;

  // Main sendMessage function — used by send button and chips
  async function sendMessage(message) {
    if (!message || !message.trim()) return;
    if (requestInProgress) {
      // ignore extra requests while one is in progress
      return;
    }
    requestInProgress = true;

    // clear existing recs when user explicitly asks something new
    clearRecommendations();

    // show the user message
    appendUserBubble(message);

    // show a typing bubble (temporary)
    const typingBubble = appendBotBubble("Thinking...");

    try {
      const data = await callBackend(message);

      // remove typing and display the reply
      try { typingBubble.remove(); } catch (e) { /* ignore */ }

      // normalize different backend shapes
      let replyText = "";
      if (typeof data === "string") {
        replyText = data;
      } else if (data.reply) {
        replyText = data.reply;
      } else if (data.response) {
        // older server used "response" — accept it
        replyText = data.response;
      } else if (data.error) {
        replyText = "Error: " + data.error;
      } else {
        // pretty print object if no known keys
        replyText = JSON.stringify(data, null, 2);
      }

      // avoid an all-empty reply (server might return empty JSON)
      if (!replyText || replyText.trim() === "") {
        replyText = "No response from assistant.";
      }

      appendBotBubble(replyText);

      // render recommendations if any
      const recsList = data.recommendations || data.recs || data.suggestions || [];
      renderRecommendations(Array.isArray(recsList) ? recsList : []);
    } catch (err) {
      try { typingBubble.remove(); } catch (e) {}
      appendBotBubble("Sorry — error contacting server. Check server logs.");
      console.error("sendMessage error:", err);
    } finally {
      requestInProgress = false;
    }
  }

  // Hook send button and Enter key
  sendBtn.addEventListener("click", () => {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendMessage(text);
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendBtn.click();
    }
  });

  // Keep setExample for compatibility with your HTML chips
  window.setExample = (q) => {
    input.value = q;
    input.focus();
  };

  // Expose sendMessage globally (optional)
  window.sendMessage = sendMessage;

  // Minimal fallback styles if your CSS doesn't include rec styling
  (function ensureStyles(){
    if (document.querySelector("style[data-app-js]")) return;
    const s = document.createElement("style");
    s.setAttribute("data-app-js","1");
    s.innerHTML = `
      #recs { display:flex; gap:8px; padding:8px 12px; flex-wrap:wrap; border-top:1px solid #f3f3f3; }
      .rec-chip { cursor:pointer; background:#eef6ff; padding:8px 12px; border-radius:999px; border:none; font-weight:600; }
    `;
    document.head.appendChild(s);
  })();

})();
