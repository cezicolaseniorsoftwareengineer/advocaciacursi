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
    console.log("🚀 Iniciando DrEstevaoChat com endpoint:", this.backendUrl);
    this.init();
  }

  async init() {
    try {
      this.createStyles();
      this.createHTML();
      this.attachEventListeners();
      await this.startNewSession();
      this.isInitialized = true;
      console.log("✅ Chat widget inicializado com sucesso");
    } catch (error) {
      console.error("❌ Erro ao inicializar chat:", error);
    }
  }

  createStyles() {
    const styles = `
      /* Chat Widget Styles */
      #dr-estevao-chat-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 50%;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        cursor: pointer;
        transition: all 0.3s ease;
        opacity: 1;
        pointer-events: auto;
      }

      #dr-estevao-chat-widget:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.6);
      }

      #dr-estevao-chat-widget .chat-button-icon {
        font-size: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
      }

      #dr-estevao-chat-widget.open {
        width: 400px;
        height: 600px;
        border-radius: 12px;
        background: linear-gradient(135deg, #0a0d11 0%, #1a1f2e 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        flex-direction: column;
      }

      #dr-estevao-chat-widget.open .chat-button-icon {
        display: none;
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

      .whatsapp-button {
        background: linear-gradient(135deg, #25d366 0%, #10b981 100%);
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: opacity 0.2s ease;
        width: 100%;
        margin-top: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }

      .whatsapp-button:hover {
        opacity: 0.9;
      }

      @media (max-width: 640px) {
        #dr-estevao-chat-widget.open {
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

    widget.innerHTML = `
      <div class="chat-button-icon">💬</div>
      <div class="chat-header">
        <div class="header-info">
          <h3>Dr. Estevão</h3>
          <span class="attendance-24h">⏰ Atendimento 24h</span>
        </div>
        <button class="chat-close-btn">✕</button>
      </div>
      <div class="chat-messages"></div>
      <div class="chat-input-area">
        <input type="text" class="chat-input" placeholder="Sua pergunta..." />
        <button class="chat-send-btn">💬</button>
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
    const buttonIcon = widget.querySelector(".chat-button-icon");

    // Toggle open/close ao clicar no ícone ou header
    buttonIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      if (!this.isOpen) {
        this.open();
      }
    });

    closeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      this.close();
    });

    // Send message
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
      console.log("📡 Tentando conectar ao backend:", this.backendUrl);
      const response = await fetch(`${this.backendUrl}/init`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        throw new Error(`Backend returned ${response.status}`);
      }

      const data = await response.json();
      this.sessionToken = data.session_token;
      console.log(
        "✅ Sessão criada:",
        this.sessionToken.substring(0, 8) + "...",
      );
      this.addMessage("assistant", data.message);
    } catch (error) {
      console.error("❌ Erro ao conectar backend:", error);
      // Modo offline - usar mock responses
      this.sessionToken = "offline-" + Date.now();
      this.isOfflineMode = true;
      this.addMessage(
        "assistant",
        "Olá! Sou o Dr. Estevão! 👋\n\nDesculpe, estou em modo offline, mas você pode sim enviar sua pergunta e ela será encaminhada para meu WhatsApp para resposta!",
      );
    }
  }

  async sendMessage(text) {
    if (!text.trim() || !this.sessionToken) return;

    const widget = document.getElementById("dr-estevao-chat-widget");
    const input = widget.querySelector(".chat-input");

    this.addMessage("user", text);
    input.value = "";

    // Se está em modo offline, sugerir contato direto
    if (this.isOfflineMode) {
      setTimeout(() => {
        this.addMessage(
          "assistant",
          "Sua mensagem será enviada diretamente para meu WhatsApp. Gostaria que eu anotasse seus dados para que eu possa responder?",
        );
        this.showContactPrompt();
      }, 500);
      return;
    }

    try {
      console.log("📤 Enviando mensagem...");
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

      // Se Dr. Estevão sugeriu contato, mostrar formulário
      if (data.suggests_contact) {
        setTimeout(() => this.showContactPrompt(), 800);
      }
    } catch (error) {
      console.error("❌ Erro ao enviar mensagem:", error);
      this.addMessage(
        "assistant",
        "Houve um erro ao processar sua mensagem. Você pode tentar novamente ou enviar diretamente pelo WhatsApp.",
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
      <div style="width: 100%; padding: 12px; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
        <p style="margin: 0 0 12px; color: #a5b4fc; font-size: 13px; font-weight: 600;">Para agendar sua consulta:</p>
        <input type="text" class="contact-name" placeholder="Seu nome completo" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box;" />
        <input type="email" class="contact-email" placeholder="Seu e-mail" style="width: 100%; padding: 8px; margin-bottom: 8px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box;" />
        <input type="tel" class="contact-phone" placeholder="Seu WhatsApp" style="width: 100%; padding: 8px; margin-bottom: 12px; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 6px; background: rgba(15, 23, 42, 0.8); color: white; box-sizing: border-box;" />
        <button class="contact-submit whatsapp-button" style="background: linear-gradient(135deg, #25d366 0%, #10b981 100%); color: white; border: none; padding: 10px; border-radius: 6px; cursor: pointer;">📱 Enviar para WhatsApp</button>
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

        // Criar mensagem formatada para WhatsApp
        const message = `Olá Dr. Estevão! Meu nome é ${name}, meu e-mail é ${email} e gostaria de agendar uma consulta. Meu WhatsApp: ${phone}`;
        const whatsappUrl = `https://wa.me/5511985773185?text=${encodeURIComponent(message)}`;

        // Abrir WhatsApp
        window.open(whatsappUrl, "_blank");

        // Salvar contato no backend (para registro)
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
            "✅ Seu contato foi salvo! Espero conversar com você no WhatsApp!",
          );
          formEl.remove();
        } catch (error) {
          console.error("Error saving contact:", error);
          // Mesmo que falhe, o WhatsApp já foi aberto
        }
      });
  }

  open() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.add("open");
    widget.style.width = "400px";
    widget.style.height = "600px";
    widget.style.borderRadius = "12px";

    const input = widget.querySelector(".chat-input");
    setTimeout(() => input.focus(), 300);

    this.isOpen = true;
  }

  close() {
    const widget = document.getElementById("dr-estevao-chat-widget");
    widget.classList.remove("open");
    widget.style.width = "60px";
    widget.style.height = "60px";
    widget.style.borderRadius = "50%";

    this.isOpen = false;
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}
