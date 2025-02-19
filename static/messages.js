document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".input-container");
  const messageContainer = document.getElementById("message-container");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");
  const userAvatar = document.querySelector(".profile-photo");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
  });

  function removeAccents(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }

  sendButton.addEventListener("click", function () {
    const message = removeAccents(userInput.value.trim().toLowerCase());
    if (message) {
      sendButton.disabled = true;
      addUserMessage(message);
      userInput.value = "";

      fetch("/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message }),
      })
        .then((response) => response.json())
        .then((data) => {
          addAIMessage(data.response);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }

  });

  function addUserMessage(message) {
    const element = `
    <div class="message user">
      <div class="user-message">
          <p>${message}</p>
      </div>
      <img class="avatar" src="${userAvatar.src}">
    </div>
    `;
    messageContainer.insertAdjacentHTML("beforeend", element);
  }

  function addAIMessage(message) {
    const element = `
    <div class="message ai">
      <img class="avatar" src="../static/images/avatar.png">
      <div class="ai-message">
        <p></p>
      </div>
    </div>
    `;
    messageContainer.insertAdjacentHTML("beforeend", element);
    const lastMessage = messageContainer.lastElementChild.querySelector(".ai-message p");
    typeText(lastMessage, message);
  }

  function typeText(element, text, i = 0) {
    if (i < text.length) {
      element.textContent = text.substring(0, i + 1) + " |";
      setTimeout(() => typeText(element, text, i + 1), 50);
    } else {
      sendButton.disabled = false;
      element.textContent = text;
    }
  }
});
