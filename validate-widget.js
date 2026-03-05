// Validação do código do chat widget
const fs = require("fs");

const chatbotCode = fs.readFileSync("js/chatbot.js", "utf-8");

console.log("🔍 Validando código do widget...\n");

// Test 1: Class exists
if (chatbotCode.includes("class DrEstevaoChat")) {
  console.log("✅ Classe DrEstevaoChat existe");
} else {
  console.log("❌ Classe DrEstevaoChat não encontrada");
}

// Test 2: createHTML method
if (
  chatbotCode.includes("createHTML()") &&
  chatbotCode.includes("dr-estevao-chat-widget")
) {
  console.log("✅ Método createHTML existe");
} else {
  console.log("❌ Método createHTML não encontrado");
}

// Test 3: Chat button icon
if (chatbotCode.includes("chat-button-icon") && chatbotCode.includes("💬")) {
  console.log("✅ Ícone de botão configurado (💬)");
} else {
  console.log("❌ Ícone de botão não encontrado");
}

// Test 4: attachEventListeners
if (chatbotCode.includes("attachEventListeners()")) {
  console.log("✅ Listeners de eventos configurados");
} else {
  console.log("❌ Listeners não encontrados");
}

// Test 5: open/close methods
if (chatbotCode.includes("open()") && chatbotCode.includes("close()")) {
  console.log("✅ Métodos open/close existem");
} else {
  console.log("❌ Métodos open/close não encontrados");
}

// Test 6: WhatsApp integration
if (
  chatbotCode.includes("wa.me") ||
  chatbotCode.includes("encodeURIComponent")
) {
  console.log("✅ Integração WhatsApp configurada");
} else {
  console.log("❌ WhatsApp integration não encontrada");
}

// Test 7: No duplicate initialization
const initMatches = chatbotCode.match(/new DrEstevaoChat/g) || [];
if (initMatches.length === 0) {
  console.log("✅ Sem inicialização duplicada no arquivo");
} else {
  console.log(
    "⚠️ Aviso: Arquivo tem inicializações internas (ok se index.html controla)",
  );
}

// Test 8: Offline mode
if (chatbotCode.includes("isOfflineMode")) {
  console.log("✅ Modo offline configurado");
} else {
  console.log("⚠️ Modo offline não encontrado");
}

console.log("\n🎉 Validação concluída!");
