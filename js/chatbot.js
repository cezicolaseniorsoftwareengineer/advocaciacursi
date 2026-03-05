/**
 * Dr. Estevão AI Chat Widget
 * Cloud icon with tooltip "Atendimento 24h"
 * Fully responsive, no emojis
 */

class DrEstevaoChat {
  constructor(config = {}) {
    this.backendUrl = config.backendUrl || "http://localhost:8000/api/v1/chat";
    this.sessionToken = null;
    this.isOpen = false;
    this.isInitialized = false;
    this.isOfflineMode = false;
    console.log("Iniciando DrEstevaoChat com endpoint:", this.backendUrl);
    this.init();
  }

  async init() {
    try {
      this.createStyles();
      this.createHTML();
      this.attachEventListeners();
      await this.startNewSession();
      this.isInitialized = true;
      console.log("Chat widget inicializado com sucesso");
    } catch (error) {
      console.error("Erro ao inicializar chat:", error);
    }
  }

  createStyles() {
    const styles = `
      /* Chat Widget - Cloud Icon */
      #dr-estevao-chat-widget {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      }

      .chat-cloud-button {
        position: relative;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border: none;
        border-radius: 30px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        padding: 0;
      }

      .chat-cloud-button:hover {
        transform: scale(1.1);
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.5);
      }

      .chat-cloud-button:active {
        transform: scale(0.95);
      }

      /* Cloud SVG Icon */
      .cloud-icon {
        width: 32px;
        height: 32px;
        fill: white;
      }

      /* Tooltip - "Atendimento 24h" */
      .chat-tooltip {
        position: absolute;
        bottom: 80px;
        right: 0;
        background: rgba(10, 13, 17, 0.95);
        color: white;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
        white-space: nowrap;
        border: 1px solid rgba(59, 130, 246, 0.3);
        opacity: 0;
        pointer-events: none;
        transform: translateY(10px);
        transition: all 0.2s ease;
        letter-spacing: 0.3px;
      }

      .chat-cloud-button:hover .chat-tooltip {
        opacity: 1;
        transform: translateY(-5px);
      }

      /* Chat Window */
      #dr-estevao-chat-widget.open .chat-cloud-button {
        display: none;
      }

      .chat-window {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 420px;
        height: 600px;
        background: linear-gradient(135deg, #0a0d11 0%, #1a1f2e 100%);
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        display: none;
        flex-direction: column;
        opacity: 0;
        transform: translateY(20px) scale(0.95);
        transition: opacity 0.3s ease, transform 0.3s ease;
        z-index: 10001;
      }

      #dr-estevao-chat-widget.open .chat-window {
        display: flex;
        opacity: 1;
        transform: translateY(0) scale(1);
      }

      .chat-header {
        padding: 18px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px 12px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
      }

      .chat-header-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0;
      }

      .chat-header-subtitle {
        font-size: 12px;
        opacity: 0.9;
        margin: 4px 0 0 0;
      }

      .chat-close-btn {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 24px;
        padding: 0;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.2s ease;
      }

      .chat-close-btn:hover {
        transform: rotate(90deg);
      }

      .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .chat-messages::-webkit-scrollbar {
        width: 6px;
      }

      .chat-messages::-webkit-scrollbar-track {
        background: transparent;
      }

      .chat-messages::-webkit-scrollbar-thumb {
        background: rgba(59, 130, 246, 0.3);
        border-radius: 3px;
      }

      .chat-messages::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.5);
      }

      .chat-message {
        display: flex;
        gap: 10px;
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
        font-size: 13px;
        font-weight: 600;
      }

      .message-avatar.user {
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #a5b4fc;
      }

      .message-content {
        flex: 1;
        padding: 10px 12px;
        border-radius: 8px;
        line-height: 1.5;
        font-size: 14px;
        word-wrap: break-word;
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
        margin-left: 38px;
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
        background: rgba(15, 23, 42, 0.6);
        color: white;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 14px;
        transition: border-color 0.2s ease;
      }

      .chat-input:focus {
        outline: none;
        border-color: rgba(59, 130, 246, 0.5);
        background: rgba(15, 23, 42, 0.8);
      }

      .chat-input::placeholder {
        color: rgba(255, 255, 255, 0.4);
      }

      .chat-send-btn {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 10px 18px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.2s ease;
      }

      .chat-send-btn:hover {
        opacity: 0.9;
        transform: translateY(-1px);
      }

      .chat-send-btn:active {
        transform: translateY(1px);
      }

      .whatsapp-button {
        background: linear-gradient(135deg, #25d366 0%, #10b981 100%);
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 13px;
        width: 100%;
        margin-top: 8px;
        transition: all 0.2s ease;
      }

      .whatsapp-button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
      }

      /* Responsive Design */
      @media (max-width: 1024px) {
        .chat-window {
          width: 380px;
          height: 550px;
          bottom: 90px;
          right: 20px;
        }
      }

      @media (max-width: 768px) {
        #dr-estevao-chat-widget {
          bottom: 20px;
          right: 20px;
          left: auto;
          top: auto;
        }

        .chat-cloud-button {
          width: 56px;
          height: 56px;
          border-radius: 28px;
        }

        .chat-window {
          width: calc(100vw - 40px);
          max-width: 360px;
          height: 70vh;
          max-height: 500px;
          bottom: 80px;
          right: 20px;
          border-radius: 12px;
        }

        .chat-cloud-button:hover .chat-tooltip {
          display: none;
        }

        .chat-tooltip {
          display: none;
        }
      }

      @media (max-width: 640px) {
        #dr-estevao-chat-widget {
          bottom: 16px;
          right: 16px;
          left: auto;
          top: auto;
        }

        .chat-cloud-button {
          width: 54px;
          height: 54px;
          border-radius: 27px;
        }

        .chat-window {
          width: calc(100vw - 32px);
          max-width: 340px;
          height: 65vh;
          max-height: 480px;
          bottom: 75px;
          right: 16px;
          border-radius: 12px;
        }

        .chat-header {
          padding: 14px;
        }

        .chat-header-title {
          font-size: 15px;
        }

        .chat-messages {
          padding: 12px;
        }

        .chat-input-area {
          padding: 10px;
        }

        .chat-close-btn {
          font-size: 20px;
        }
      }

      @media (max-width: 480px) {
        #dr-estevao-chat-widget {
          bottom: 12px;
          right: 12px;
          left: auto;
          top: auto;
        }

        .chat-cloud-button {
          width: 52px;
          height: 52px;
          border-radius: 26px;
        }

        .chat-window {
          width: calc(100vw - 24px);
          max-width: 320px;
          height: 60vh;
          max-height: 450px;
          bottom: 70px;
          right: 12px;
          border-radius: 12px;
        }

        .chat-header {
          padding: 12px;
        }

        .chat-header-title {
          font-size: 14px;
        }

        .chat-messages {
          padding: 10px;
        }

        .chat-input-area {
          padding: 8px;
        }

        .chat-input {
          font-size: 13px;
        }

        .chat-send-btn {
          font-size: 12px;
          padding: 8px 12px;
        }

        .chat-close-btn {
          font-size: 18px;
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

    widget.innerHTML = `
      <button class="chat-cloud-button" aria-label="Abrir chat de atendimento">
        <svg class="cloud-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4c-1.48 0-2.85.43-4.01 1.17-.5.35-1.02-.21-1.02-.79 0-2.65 2.05-4.8 4.59-4.8 2.29 0 4.25 1.54 4.81 3.63.98-.04 1.95.19 2.84.77 1.08-.88 2.49-1.4 4.02-1.4 3.31 0 6 2.69 6 6 0 .5-.08.99-.2 1.46.62.37 1.2.82 1.69 1.35C23.5 14.5 23 15 22.45 15H2.57c-.64 0-1.21-.56-1.21-1.25 0-.65.56-1.21 1.21-1.21h.13c.04-.31.12-.61.25-.89C2.08 10.4 1 8.86 1 7.08 1 5.42 2.15 4 3.58 4c1.02 0 1.93.6 2.4 1.47.72-.29 1.51-.45 2.34-.45 4.41 0 8 3.59 8 8 0 .37-.03.73-.08 1.09z"/>
        </svg>
        <div class="chat-tooltip">Atendimento 24h</div>
      </button>

      <div class="chat-window">
        <div class="chat-header">
          <div>
            <h3 class="chat-header-title">Dr. Estevão</h3>
            <p class="chat-header-subtitle">Atendimento 24h</p>
          </div>
          <button class="chat-close-btn" aria-label="Fechar chat" title="Fechar">×</button>
        </div>
        <div class="chat-messages"></div>
        <div class="chat-input-area">
          <input type="text" class="chat-input" placeholder="Sua pergunta..." />
          <button class="chat-send-btn">Enviar</button>
        </div>
      </div>
    `;

    document.body.appendChild(widget);
  }

  attachEventListeners() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    const cloudButton = widget.querySelector(".chat-cloud-button");
    const closeBtn = widget.querySelector(".chat-close-btn");
    const input = widget.querySelector(".chat-input");
    const sendBtn = widget.querySelector(".chat-send-btn");

    cloudButton.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!this.isOpen) {
        this.open();
      }
    });

    closeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      this.close();
    });

    sendBtn.addEventListener("click", () => {
      if (input.value.trim()) {
        this.sendMessage(input.value);
      }
    });

    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && input.value.trim()) {
        this.sendMessage(input.value);
      }
    });
  }

  async startNewSession() {
    try {
      console.log("Conectando ao backend:", this.backendUrl);
      const response = await fetch(`${this.backendUrl}/init`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      this.sessionToken = data.session_token;
      console.log("Sessão criada:", this.sessionToken.substring(0, 8) + "...");
      this.addMessage("assistant", data.message);
    } catch (error) {
      console.error("Erro ao conectar backend:", error);
      this.sessionToken = "offline-" + Date.now();
      this.isOfflineMode = true;
      this.addMessage(
        "assistant",
        "Olá! Sou o Dr. Estevão!\n\nDesculpe, estou em modo offline, mas você pode enviar sua pergunta e ela será encaminhada para meu WhatsApp para resposta!",
      );
    }
  }

  async sendMessage(text) {
    if (!text.trim() || !this.sessionToken) return;

    const widget = document.getElementById("dr-estevao-chat-widget");
    const input = widget.querySelector(".chat-input");

    this.addMessage("user", text);
    input.value = "";

    if (this.isOfflineMode) {
      setTimeout(() => {
        this.addMessage(
          "assistant",
          "Sua mensagem será encaminhada para meu WhatsApp. Gostaria que eu anotasse seus dados?",
        );
        this.showContactPrompt();
      }, 500);
      return;
    }

    try {
      console.log("Enviando mensagem...");
      const response = await fetch(`${this.backendUrl}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_token: this.sessionToken,
          message: text,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      this.addMessage("assistant", data.response);

      if (data.suggests_contact) {
        setTimeout(() => this.showContactPrompt(), 800);
      }
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      this.addMessage(
        "assistant",
        "Houve um erro ao processar sua mensagem. Tente novamente ou envie pelo WhatsApp.",
      );
    }
  }

  addMessage(role, content) {
    const messagesDiv = document
      .getElementById("dr-estevao-chat-widget")
      .querySelector(".chat-messages");

    const messageEl = document.createElement("div");
    messageEl.className = "chat-message";
    const avatar = role === "user" ? "Você" : "Dr.E";
    messageEl.innerHTML = `
      <div class="message-avatar ${role}">${avatar}</div>
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
        <button class="contact-btn-yes" style="background: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; margin-right: 8px; font-size: 12px;">Sim</button>
        <button class="contact-btn-no" style="background: transparent; color: #a5b4fc; border: 1px solid rgba(59, 130, 246, 0.3); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 12px;">Depois</button>
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
      <div style="width: 100%; padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
        <p style="margin: 0 0 12px; color: #a5b4fc; font-size: 12px; font-weight: 600;">Para agendar sua consulta:</p>
        <input type="text" class="contact-name" placeholder="Seu nome completo" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box; font-size: 13px;" />
        <input type="email" class="contact-email" placeholder="Seu e-mail" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box; font-size: 13px;" />
        <input type="tel" class="contact-phone" placeholder="Seu WhatsApp" style="width: 100%; padding: 8px; margin-bottom: 12px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box; font-size: 13px;" />
        <button class="contact-submit whatsapp-button">Enviar para WhatsApp</button>
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

        const message = `Olá Dr. Estevão! Meu nome é ${name}, meu e-mail é ${email} e gostaria de agendar uma consulta. Meu WhatsApp: ${phone}`;
        const whatsappUrl = `https://wa.me/5511985773185?text=${encodeURIComponent(message)}`;

        window.open(whatsappUrl, "_blank");

        try {
          await fetch(`${this.backendUrl}/contact`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              session_token: this.sessionToken,
              client_name: name,
              client_email: email,
              client_phone: phone,
            }),
          });

          this.addMessage(
            "assistant",
            "Seu contato foi salvo! Espero conversar com você no WhatsApp!",
          );
          formEl.remove();
        } catch (error) {
          console.error("Erro ao salvar contato:", error);
        }
      });
  }

  open() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.add("open");
    this.isOpen = true;
    const input = widget.querySelector(".chat-input");
    setTimeout(() => input.focus(), 300);
  }

  close() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.remove("open");
    this.isOpen = false;
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}
