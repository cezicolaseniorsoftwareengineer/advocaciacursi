/**
 * Dr. Estevão AI Chat Widget
 * Retractable chat component integrated with FastAPI backend
 */

class DrEstevaoChat {
  constructor(config = {}) {
    this.backendUrl = config.backendUrl || "http://localhost:8000/api/v1/chat";
    this.sessionToken = null;
    this.isOpen = false;
    this.isInitialized = false;
    this.init();
  }

  async init() {
    this.createStyles();
    this.createHTML();
    this.attachEventListeners();
    await this.startNewSession();
    this.isInitialized = true;
  }

  createStyles() {
    const styles = `
      /* Chat Widget Styles */
      #dr-estevao-chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 380px;
        max-width: 90vw;
        height: 600px;
        max-height: 80vh;
        background: linear-gradient(135deg, #0a0d11 0%, #1a1f2e 100%);
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.2);
        display: flex;
        flex-direction: column;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        opacity: 0;
        transform: translateY(20px) scale(0.95);
        transition: opacity 0.3s ease, transform 0.3s ease;
        pointer-events: none;
      }

      #dr-estevao-chat-widget.open {
        opacity: 1;
        transform: translateY(0) scale(1);
        pointer-events: auto;
      }

      #dr-estevao-chat-widget.closed {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        cursor: pointer;
      }

      .chat-header {
        padding: 16px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .chat-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }

      .chat-header .header-info {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .chat-header .attendance-24h {
        font-size: 12px;
        opacity: 0.9;
        font-weight: 400;
      }

      .chat-close-btn {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 20px;
        padding: 0;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .chat-message {
        display: flex;
        gap: 8px;
        animation: messageSlideIn 0.3s ease;
      }

      @keyframes messageSlideIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .message-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 14px;
      }

      .message-avatar.user {
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.3);
      }

      .message-content {
        flex: 1;
        padding: 10px 12px;
        border-radius: 8px;
        line-height: 1.4;
        font-size: 14px;
      }

      .message-content.assistant {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.2);
        color: #e0e7ff;
      }

      .message-content.user {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #e0e7ff;
        margin-left: 30px;
      }

      .chat-input-area {
        padding: 12px;
        border-top: 1px solid rgba(59, 130, 246, 0.1);
        display: flex;
        gap: 8px;
      }

      .chat-input {
        flex: 1;
        border: 1px solid rgba(59, 130, 246, 0.2);
        background: rgba(15, 23, 42, 0.5);
        color: white;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 14px;
      }

      .chat-input::placeholder {
        color: rgba(255, 255, 255, 0.5);
      }

      .chat-send-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: opacity 0.2s ease;
      }

      .chat-send-btn:hover {
        opacity: 0.9;
      }

      @media (max-width: 640px) {
    #dr-estevao-chat-widget {
      width: 100vw;
      height: 100vh;
      bottom: 0;
      right: 0;
      border-radius: 0;
      max-height: 100vh;
    }

    .chat-messages {
      padding: 12px;
    }

    .chat-input-area {
      padding: 8px;
    }
  }
    `;

    const styleTag = document.createElement("style");
    styleTag.textContent = styles;
    document.head.appendChild(styleTag);
  }

  createHTML() {
    const widget = document.createElement("div");
    widget.id = "dr-estevao-chat-widget";
    widget.className = "closed";
    widget.innerHTML = `
      <div class="chat-header" style="display: none;">
        <div class="header-info">
          <h3>💬 Dr. Estevão</h3>
          <span class="attendance-24h">Atendimento 24h</span>
        </div>
        <button class="chat-close-btn">✕</button>
      </div>
      <div class="chat-messages" style="display: none;"></div>
      <div class="chat-input-area" style="display: none;">
        <input type="text" class="chat-input" placeholder="Sua mensagem..." />
        <button class="chat-send-btn">Enviar</button>
      </div>
    `;

    document.body.appendChild(widget);
  }

  attachEventListeners() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    const header = widget.querySelector(".chat-header");
    const closeBtn = widget.querySelector(".chat-close-btn");
    const input = widget.querySelector(".chat-input");
    const sendBtn = widget.querySelector(".chat-send-btn");

    // Toggle open/close
    widget.addEventListener("click", (e) => {
      if (
        !this.isOpen &&
        !e.target.closest(".chat-header") &&
        !e.target.closest(".chat-messages") &&
        !e.target.closest(".chat-input-area")
      ) {
        this.open();
      }
    });

    closeBtn.addEventListener("click", () => this.close());

    // Send message
    sendBtn.addEventListener("click", () => this.sendMessage(input.value));
    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        this.sendMessage(input.value);
      }
    });
  }

  async startNewSession() {
    try {
      const response = await fetch(`${this.backendUrl}/init`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await response.json();
      this.sessionToken = data.session_token;
      this.addMessage("assistant", data.message);
    } catch (error) {
      console.error("Error starting chat session:", error);
      this.addMessage(
        "assistant",
        "Desculpe, ocorreu um erro ao inicializar o chat. Tente novamente.",
      );
    }
  }

  async sendMessage(text) {
    if (!text.trim() || !this.sessionToken) return;

    const widget = document.getElementById("dr-estevao-chat-widget");
    const input = widget.querySelector(".chat-input");

    this.addMessage("user", text);
    input.value = "";

    try {
      const response = await fetch(`${this.backendUrl}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_token: this.sessionToken,
          message: text,
        }),
      });

      const data = await response.json();
      this.addMessage("assistant", data.response);

      // Se Dr. Estevão sugeriu contato, mostrar botão de contato
      if (data.suggests_contact) {
        this.showContactPrompt();
      }
    } catch (error) {
      console.error("Error sending message:", error);
      this.addMessage(
        "assistant",
        "Desculpe, ocorreu um erro ao processar sua mensagem.",
      );
    }
  }

  addMessage(role, content) {
    const messagesDiv = document
      .getElementById("dr-estevao-chat-widget")
      .querySelector(".chat-messages");

    const messageEl = document.createElement("div");
    messageEl.className = "chat-message";
    messageEl.innerHTML = `
      <div class="message-avatar ${role}">${role === "user" ? "👤" : "⚖️"}</div>
      <div class="message-content ${role}">${this.escapeHtml(content)}</div>
    `;

    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  showContactPrompt() {
    const messagesDiv = document
      .getElementById("dr-estevao-chat-widget")
      .querySelector(".chat-messages");

    const promptEl = document.createElement("div");
    promptEl.className = "chat-message";
    promptEl.innerHTML = `
      <div style="width: 100%; text-align: center; padding: 12px 0;">
        <p style="margin: 0 0 8px; color: #a5b4fc; font-size: 13px;">Deseja agendar uma consulta?</p>
        <button class="contact-btn-yes" style="background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-right: 8px;">Sim</button>
        <button class="contact-btn-no" style="background: transparent; color: #a5b4fc; border: 1px solid rgba(59, 130, 246, 0.3); padding: 8px 16px; border-radius: 6px; cursor: pointer;">Depois</button>
      </div>
    `;

    messagesDiv.appendChild(promptEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    promptEl.querySelector(".contact-btn-yes").addEventListener("click", () => {
      this.showContactForm();
      promptEl.remove();
    });

    promptEl.querySelector(".contact-btn-no").addEventListener("click", () => {
      promptEl.remove();
    });
  }

  showContactForm() {
    const messagesDiv = document
      .getElementById("dr-estevao-chat-widget")
      .querySelector(".chat-messages");

    const formEl = document.createElement("div");
    formEl.className = "chat-message";
    formEl.innerHTML = `
      <div style="width: 100%; padding: 12px;">
        <input type="text" class="contact-name" placeholder="Seu nome completo" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.5); color: white;" />
        <input type="email" class="contact-email" placeholder="Seu e-mail" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.5); color: white;" />
        <input type="tel" class="contact-phone" placeholder="Seu telefone" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.5); color: white;" />
        <button class="contact-submit" style="width: 100%; background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer; margin-top: 8px;">Enviar Solicitud</button>
      </div>
    `;

    messagesDiv.appendChild(formEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    formEl
      .querySelector(".contact-submit")
      .addEventListener("click", async () => {
        const name = formEl.querySelector(".contact-name").value;
        const email = formEl.querySelector(".contact-email").value;
        const phone = formEl.querySelector(".contact-phone").value;

        if (!name || !email || !phone) {
          alert("Por favor, preencha todos os campos.");
          return;
        }

        try {
          const response = await fetch(`${this.backendUrl}/contact`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              session_token: this.sessionToken,
              client_name: name,
              client_email: email,
              client_phone: phone,
            }),
          });

          const data = await response.json();
          if (data.success) {
            this.addMessage("assistant", data.message);
            formEl.remove();
          }
        } catch (error) {
          console.error("Error submitting contact:", error);
          alert("Erro ao enviar. Tente novamente.");
        }
      });
  }

  open() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.remove("closed");
    widget.classList.add("open");

    widget.querySelector(".chat-header").style.display = "flex";
    widget.querySelector(".chat-messages").style.display = "flex";
    widget.querySelector(".chat-input-area").style.display = "flex";

    this.isOpen = true;
    widget.querySelector(".chat-input").focus();
  }

  close() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.add("closed");
    widget.classList.remove("open");

    widget.querySelector(".chat-header").style.display = "none";
    widget.querySelector(".chat-messages").style.display = "none";
    widget.querySelector(".chat-input-area").style.display = "none";

    this.isOpen = false;
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

// Inicializar o chat quando o documento estiver pronto
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    new DrEstevaoChat({ backendUrl: "http://localhost:8000/api/v1/chat" });
  });
} else {
  new DrEstevaoChat({ backendUrl: "http://localhost:8000/api/v1/chat" });
}
