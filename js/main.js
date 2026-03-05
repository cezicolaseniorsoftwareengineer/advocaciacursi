/**
 * CEZI COLA DESIGN SYSTEM — Dr. Estevão Cursi Advocacia
 * Main JavaScript Module
 * @description Mobile navigation, scroll effects, accessibility
 */

(function () {
  "use strict";

  // ============================================================
  // MOBILE NAVIGATION
  // ============================================================

  const initMobileNav = () => {
    const navToggle = document.querySelector(".nav__toggle");
    const navMenu = document.querySelector(".nav__menu");
    const navLinks = document.querySelectorAll(".nav__link");

    if (!navToggle || !navMenu) return;

    navToggle.addEventListener("click", () => {
      navToggle.classList.toggle("active");
      navMenu.classList.toggle("active");

      // Accessibility
      const isExpanded = navMenu.classList.contains("active");
      navToggle.setAttribute("aria-expanded", isExpanded);
      document.body.style.overflow = isExpanded ? "hidden" : "";
    });

    // Close menu on link click
    navLinks.forEach((link) => {
      link.addEventListener("click", () => {
        navToggle.classList.remove("active");
        navMenu.classList.remove("active");
        navToggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      });
    });

    // Close menu on ESC key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && navMenu.classList.contains("active")) {
        navToggle.classList.remove("active");
        navMenu.classList.remove("active");
        navToggle.setAttribute("aria-expanded", "false");
        document.body.style.overflow = "";
      }
    });
  };

  // ============================================================
  // SCROLL EFFECTS
  // ============================================================

  const initScrollEffects = () => {
    const header = document.querySelector(".header");
    if (!header) return;

    let lastScroll = 0;

    window.addEventListener("scroll", () => {
      const currentScroll = window.pageYOffset;

      // Add shadow on scroll
      if (currentScroll > 50) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }

      lastScroll = currentScroll;
    });
  };

  // ============================================================
  // SMOOTH SCROLL
  // ============================================================

  const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");

        // Ignore # only links
        if (href === "#") {
          e.preventDefault();
          return;
        }

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const header = document.querySelector(".header");
          const headerOffset = header ? header.offsetHeight : 80;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition =
            elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth",
          });
        }
      });
    });
  };

  // ============================================================
  // INTERSECTION OBSERVER (Fade-in on scroll)
  // ============================================================

  const initIntersectionObserver = () => {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }
      });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll(".card").forEach((card) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(30px)";
      card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      observer.observe(card);
    });
  };

  // ============================================================
  // FORM VALIDATION (Contact forms)
  // ============================================================

  const initFormValidation = () => {
    const forms = document.querySelectorAll("form[data-validate]");

    forms.forEach((form) => {
      form.addEventListener("submit", (e) => {
        e.preventDefault();

        let isValid = true;
        const inputs = form.querySelectorAll(
          "input[required], textarea[required], select[required]",
        );

        inputs.forEach((input) => {
          if (!input.value.trim()) {
            isValid = false;
            input.classList.add("error");
            input.setAttribute("aria-invalid", "true");
          } else {
            input.classList.remove("error");
            input.setAttribute("aria-invalid", "false");
          }
        });

        if (isValid) {
          const leadData = {
            nome: form.querySelector("#nome")?.value || "Não informado",
            email: form.querySelector("#email")?.value || "Não informado",
            telefone: form.querySelector("#telefone")?.value || "Não informado",
            mensagem: form.querySelector("#mensagem")?.value || "Não informado",
            area: form.querySelector("#area")?.value || "Contato Geral",
          };

          // Construir e codificar a mensagem do WhatsApp
          const whatsappNumber = "5511985773185";
          const rawMessage = [
            "Olá, Dr. Estevão Cursi!",
            "",
            "Recebi um contato via formulário do site com os seguintes dados:",
            "",
            `Nome: ${leadData.nome}`,
            `E-mail: ${leadData.email}`,
            `Telefone: ${leadData.telefone}`,
            `Área de Interesse: ${leadData.area}`,
            `Mensagem: ${leadData.mensagem}`,
            "",
            "Por favor, entre em contato.",
          ].join("\n");

          const message = encodeURIComponent(rawMessage);
          const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${message}`;

          // Abrir o WhatsApp em nova aba
          window.open(whatsappUrl, "_blank");

          form.reset();
          console.log("Formulário enviado para WhatsApp:", leadData);
        }
      });
    });
  };

  // ============================================================
  // ACCESSIBILITY ENHANCEMENTS
  // ============================================================

  const initAccessibility = () => {
    // Skip to main content link
    const skipLink = document.querySelector(".skip-link");
    if (skipLink) {
      skipLink.addEventListener("click", (e) => {
        e.preventDefault();
        const main = document.querySelector("main");
        if (main) {
          main.setAttribute("tabindex", "-1");
          main.focus();
        }
      });
    }

    // Add aria-labels to interactive elements without text
    document.querySelectorAll("button:empty, a:empty").forEach((el) => {
      if (!el.getAttribute("aria-label")) {
        console.warn("Interactive element without aria-label:", el);
      }
    });
  };

  // ============================================================
  // PERFORMANCE MONITORING
  // ============================================================

  const logPerformanceMetrics = () => {
    if ("performance" in window) {
      window.addEventListener("load", () => {
        setTimeout(() => {
          const perfData = performance.getEntriesByType("navigation")[0];
          console.log("Performance Metrics:", {
            domContentLoaded:
              perfData.domContentLoadedEventEnd -
              perfData.domContentLoadedEventStart,
            loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
            domInteractive: perfData.domInteractive,
          });
        }, 0);
      });
    }
  };

  // ============================================================
  // INITIALIZATION
  // ============================================================

  const init = () => {
    initMobileNav();
    initScrollEffects();
    initSmoothScroll();
    initIntersectionObserver();
    initFormValidation();
    initAccessibility();

    // Development only
    if (
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1"
    ) {
      logPerformanceMetrics();
    }
  };

  // Wait for DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
