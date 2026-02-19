const joinPanel = document.getElementById("joinPanel");
const chatPanel = document.getElementById("chatPanel");
const usernameInput = document.getElementById("username");
const roomInput = document.getElementById("room");
const joinBtn = document.getElementById("joinBtn");
const roomTitle = document.getElementById("roomTitle");
const messages = document.getElementById("messages");
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("messageInput");

let socket;

function appendMessage(htmlClass, metaText, contentText) {
  const wrap = document.createElement("article");
  wrap.className = `message ${htmlClass}`;

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = metaText;

  const content = document.createElement("div");
  content.textContent = contentText;

  wrap.append(meta, content);
  messages.appendChild(wrap);
  messages.scrollTop = messages.scrollHeight;
}

joinBtn.addEventListener("click", () => {
  const username = usernameInput.value.trim();
  const room = roomInput.value.trim() || "general";

  if (!username) {
    alert("Введите имя");
    return;
  }

  socket = new WebSocket(`${location.origin.replace("http", "ws")}/ws`);

  socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ action: "join", username, room }));
    joinPanel.classList.add("hidden");
    chatPanel.classList.remove("hidden");
    roomTitle.textContent = `Комната #${room}`;
  });

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "system") {
      appendMessage("system", data.time, data.message);
      return;
    }

    if (data.type === "chat") {
      appendMessage("", `${data.username} • ${data.time}`, data.text);
      return;
    }

    if (data.type === "error") {
      appendMessage("system", "ошибка", data.message);
    }
  });

  socket.addEventListener("close", () => {
    appendMessage("system", "соединение", "Соединение закрыто");
  });
});

messageForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const text = messageInput.value.trim();
  if (!text || !socket || socket.readyState !== WebSocket.OPEN) {
    return;
  }

  socket.send(JSON.stringify({ action: "message", text }));
  messageInput.value = "";
});
