/**
 * ADMIN DASHBOARD - LEAD MANAGEMENT SYSTEM
 * Dr. Estevão Cursi - Bio Code Technology
 * @description Sistema de gerenciamento de leads com localStorage
 */

(function () {
  "use strict";

  // ============================================================
  // AUTH CHECK
  // ============================================================

  function checkAuth() {
    if (sessionStorage.getItem("adminAuth") !== "true") {
      window.location.href = "login.html";
      return false;
    }
    return true;
  }

  // ============================================================
  // LOGOUT
  // ============================================================

  window.logout = function () {
    if (confirm("Deseja realmente sair do sistema?")) {
      sessionStorage.removeItem("adminAuth");
      sessionStorage.removeItem("adminUser");
      sessionStorage.removeItem("loginTime");
      window.location.href = "login.html";
    }
  };

  // ============================================================
  // LEAD MANAGEMENT
  // ============================================================

  class LeadManager {
    constructor() {
      this.leads = this.loadLeads();
      this.currentFilter = "todos";
    }

    // Load leads from localStorage
    loadLeads() {
      const stored = localStorage.getItem("advocaciaLeads");
      return stored ? JSON.parse(stored) : this.getDefaultLeads();
    }

    // Get default demo leads
    getDefaultLeads() {
      return [
        {
          id: Date.now() + 1,
          nome: "João Silva",
          email: "joao.silva@email.com",
          telefone: "(11) 98765-4321",
          mensagem: "Preciso de ajuda com processo trabalhista de rescisão.",
          area: "Execução Trabalhista",
          status: "quente",
          data: new Date(Date.now() - 86400000).toISOString(), // 1 dia atrás
        },
        {
          id: Date.now() + 2,
          nome: "Maria Santos",
          email: "maria.santos@empresa.com",
          telefone: "(11) 97654-3210",
          mensagem:
            "Gostaria de contratar assessoria jurídica para minha empresa.",
          area: "Assessoria Empresas",
          status: "quente",
          data: new Date(Date.now() - 172800000).toISOString(), // 2 dias atrás
        },
        {
          id: Date.now() + 3,
          nome: "Carlos Oliveira",
          email: "carlos@email.com",
          telefone: "(11) 96543-2109",
          mensagem: "Preciso de orientação sobre defesa criminal.",
          area: "Defesa Criminal",
          status: "frio",
          data: new Date(Date.now() - 259200000).toISOString(), // 3 dias atrás
        },
        {
          id: Date.now() + 4,
          nome: "Ana Costa",
          email: "ana.costa@email.com",
          telefone: "(11) 95432-1098",
          mensagem: "Tive um erro médico e gostaria de indenização.",
          area: "Direito da Saúde",
          status: "convertido",
          data: new Date(Date.now() - 604800000).toISOString(), // 7 dias atrás
        },
      ];
    }

    // Save leads to localStorage
    saveLeads() {
      localStorage.setItem("advocaciaLeads", JSON.stringify(this.leads));
      this.updateStats();
      this.renderLeads();
    }

    // Add new lead
    addLead(leadData) {
      const newLead = {
        id: Date.now(),
        ...leadData,
        status: "frio", // Default status
        data: new Date().toISOString(),
      };
      this.leads.unshift(newLead); // Add to beginning
      this.saveLeads();
      return newLead;
    }

    // Update lead status
    updateStatus(id, newStatus) {
      const lead = this.leads.find((l) => l.id === id);
      if (lead) {
        lead.status = newStatus;
        this.saveLeads();
      }
    }

    // Delete lead
    deleteLead(id) {
      if (confirm("Deseja realmente excluir este lead?")) {
        this.leads = this.leads.filter((l) => l.id !== id);
        this.saveLeads();
      }
    }

    // Get filtered leads
    getFilteredLeads() {
      if (this.currentFilter === "todos") {
        return this.leads;
      }
      return this.leads.filter((l) => l.status === this.currentFilter);
    }

    // Update statistics
    updateStats() {
      const total = this.leads.length;
      const quentes = this.leads.filter((l) => l.status === "quente").length;
      const frios = this.leads.filter((l) => l.status === "frio").length;
      const convertidos = this.leads.filter(
        (l) => l.status === "convertido",
      ).length;

      document.getElementById("totalLeads").textContent = total;
      document.getElementById("hotLeads").textContent = quentes;
      document.getElementById("coldLeads").textContent = frios;
      document.getElementById("convertedLeads").textContent = convertidos;
    }

    // Render leads table
    renderLeads() {
      const tbody = document.getElementById("leadsTableBody");
      const filteredLeads = this.getFilteredLeads();

      if (filteredLeads.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="7">
              <div class="empty-state">
                <div class="empty-state__icon">📭</div>
                <p>Nenhum lead encontrado com este filtro.</p>
              </div>
            </td>
          </tr>
        `;
        return;
      }

      tbody.innerHTML = filteredLeads
        .map((lead) => {
          const date = new Date(lead.data);
          const dateStr = date.toLocaleDateString("pt-BR");
          const timeStr = date.toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit",
          });

          let statusClass = "lead-status--frio";
          let statusText = "Frio";

          if (lead.status === "quente") {
            statusClass = "lead-status--quente";
            statusText = "Quente";
          } else if (lead.status === "convertido") {
            statusClass = "lead-status--convertido";
            statusText = "Convertido";
          }

          return `
          <tr>
            <td>
              <div>${dateStr}</div>
              <div style="font-size: 0.8rem; color: var(--text-muted);">${timeStr}</div>
            </td>
            <td><strong>${lead.nome}</strong></td>
            <td>${lead.email}</td>
            <td>${lead.telefone}</td>
            <td>${lead.area || "Não especificado"}</td>
            <td>
              <span class="lead-status ${statusClass}">${statusText}</span>
            </td>
            <td>
              <div class="action-buttons">
                <button class="btn-small btn-view" onclick="viewLead(${lead.id})">Ver</button>
                <button class="btn-small btn-status" onclick="toggleStatus(${lead.id})">Status</button>
                <button class="btn-small btn-delete" onclick="deleteLead(${lead.id})">Excluir</button>
              </div>
            </td>
          </tr>
        `;
        })
        .join("");
    }
  }

  // ============================================================
  // GLOBAL INSTANCE
  // ============================================================

  let leadManager;

  // ============================================================
  // GLOBAL FUNCTIONS
  // ============================================================

  window.filterLeads = function (filter) {
    leadManager.currentFilter = filter;
    leadManager.renderLeads();

    // Update active tab
    document.querySelectorAll(".filter-tab").forEach((tab) => {
      tab.classList.remove("active");
    });
    event.target.classList.add("active");
  };

  window.viewLead = function (id) {
    const lead = leadManager.leads.find((l) => l.id === id);
    if (!lead) return;

    const date = new Date(lead.data);
    const dateStr = date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

    document.getElementById("leadDetails").innerHTML = `
      <div class="lead-detail">
        <p class="lead-detail__label">Nome Completo</p>
        <p class="lead-detail__value">${lead.nome}</p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">E-mail</p>
        <p class="lead-detail__value"><a href="mailto:${lead.email}">${lead.email}</a></p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">Telefone</p>
        <p class="lead-detail__value"><a href="tel:${lead.telefone.replace(/\D/g, "")}">${lead.telefone}</a></p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">Área de Interesse</p>
        <p class="lead-detail__value">${lead.area || "Não especificado"}</p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">Mensagem</p>
        <p class="lead-detail__value">${lead.mensagem || "Sem mensagem"}</p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">Data de Cadastro</p>
        <p class="lead-detail__value">${dateStr}</p>
      </div>
      <div class="lead-detail">
        <p class="lead-detail__label">Status Atual</p>
        <p class="lead-detail__value">
          <span class="lead-status lead-status--${lead.status}">
            ${lead.status === "quente" ? "Quente" : lead.status === "frio" ? "Frio" : "Convertido"}
          </span>
        </p>
      </div>
    `;

    document.getElementById("leadModal").classList.add("active");
  };

  window.closeModal = function () {
    document.getElementById("leadModal").classList.remove("active");
  };

  window.toggleStatus = function (id) {
    const lead = leadManager.leads.find((l) => l.id === id);
    if (!lead) return;

    const statusOptions = ["frio", "quente", "convertido"];
    const currentIndex = statusOptions.indexOf(lead.status);
    const nextIndex = (currentIndex + 1) % statusOptions.length;

    leadManager.updateStatus(id, statusOptions[nextIndex]);
  };

  window.deleteLead = function (id) {
    leadManager.deleteLead(id);
  };

  // ============================================================
  // INITIALIZATION
  // ============================================================

  function init() {
    // Check authentication
    if (!checkAuth()) return;

    // Set username
    const userName = sessionStorage.getItem("adminUser") || "Admin";
    document.getElementById("userName").textContent = userName;

    // Initialize lead manager
    leadManager = new LeadManager();
    leadManager.updateStats();
    leadManager.renderLeads();

    // Close modal on outside click
    document
      .getElementById("leadModal")
      .addEventListener("click", function (e) {
        if (e.target === this) {
          closeModal();
        }
      });

    // Close modal on ESC key
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        closeModal();
      }
    });
  }

  // Wait for DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Export for form integration
  window.LeadManager = LeadManager;
})();
