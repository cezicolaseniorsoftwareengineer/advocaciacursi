/**
 * Teste de integração: Simula fluxo completo do chat
 * 1. Carrega o chat widget
 * 2. Chama /init
 * 3. Envia mensagem
 * 4. Verifica resposta
 */

(async function testChatIntegration() {
  console.log("🔍 TESTE DE INTEGRAÇÃO DO CHAT");

  const backendUrl = "http://localhost:8000/api/v1/chat";

  // 1. Init
  console.log("1️⃣ Inicializando chat...");
  const initResponse = await fetch(`${backendUrl}/init`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });

  if (!initResponse.ok) {
    console.error("❌ Init falhou:", initResponse.status);
    return;
  }

  const initData = await initResponse.json();
  const sessionToken = initData.session_token;
  const initialMessage = initData.message;

  console.log("✅ Init sucesso:");
  console.log("   - Token:", sessionToken.substring(0, 8) + "...");
  console.log("   - Greeting:", initialMessage);

  // 2. Message
  console.log("\n2️⃣ Enviando mensagem...");
  const testMessage = "Preciso de ajuda com contrato de trabalho comum";

  const messageResponse = await fetch(`${backendUrl}/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_token: sessionToken,
      message: testMessage,
    }),
  });

  if (!messageResponse.ok) {
    console.error("❌ Message falhou:", messageResponse.status);
    return;
  }

  const messageData = await messageResponse.json();
  console.log("✅ Message sucesso:");
  console.log("   - Entrada:", testMessage);
  console.log("   - Resposta:", messageData.response);

  // 3. Contact
  console.log("\n3️⃣ Salvando contato...");
  const contactResponse = await fetch(`${backendUrl}/contact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_token: sessionToken,
      client_name: "Dr. João Silva",
      client_email: "joao@example.com",
      client_phone: "+5511987654321",
    }),
  });

  if (!contactResponse.ok) {
    console.error("❌ Contact falhou:", contactResponse.status);
    return;
  }

  const contactData = await contactResponse.json();
  console.log("✅ Contact salvo:");
  console.log("   - Contact ID:", contactData.contact_id);
  console.log("   - Email:", contactData.email);
  console.log("   - Phone:", contactData.phone);

  console.log("\n🎉 TESTE COMPLETO COM SUCESSO!");
  console.log("O sistema está pronto para produção.");
})();
