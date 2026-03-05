#!/usr/bin/env python3
"""
Script de teste: Fluxo completo do agente Dr. Estevão
Testa: init → qualif → deeper_qual → deeper_qual 2 → solution → contact
"""

import requests
import json
import time

BASE_URL = "http://localhost:8001/api/v1/chat"

def test_agent_flow():
    print("🤖 Testando Dr. Estevão - Fluxo Completo\n")
    print("=" * 70)

    # 1. Inicializar sessão
    print("\n1️⃣  INIT: Criando nova sessão...")
    init_resp = requests.post(f"{BASE_URL}/init", json={})
    session = init_resp.json()["session_token"]
    greeting = init_resp.json()["message"]
    print(f"✓ Sessão: {session[:12]}...")
    print(f"✓ Saudação: {greeting[:60]}...\n")

    # 2. Qualificação
    print("2️⃣  QUALIFICATION: Enviando demissão...")
    msg1 = {"session_token": session, "message": "Fui demitido sem justa causa"}
    resp1 = requests.post(f"{BASE_URL}/message", json=msg1)
    data1 = resp1.json()
    print(f"✓ Resposta: {data1['response'][:70]}...")
    print(f"✓ Stage: {data1['stage']}")
    print(f"✓ Intent: {data1.get('intent', 'N/A')}\n")

    # 3. Aprofundamento 1
    print("3️⃣  DEEPER QUALIFICATION 1: Segunda pergunta...")
    msg2 = {"session_token": session, "message": "Não recebi aviso prévio além disso"}
    resp2 = requests.post(f"{BASE_URL}/message", json=msg2)
    data2 = resp2.json()
    print(f"✓ Stage: {data2['stage']}")
    print(f"✓ Response chars: {len(data2['response'])}\n")

    # 4. Aprofundamento 2
    print("4️⃣  DEEPER QUALIFICATION 2: Terceira pergunta...")
    msg3 = {"session_token": session, "message": "Sim, tenho emails e registros"}
    resp3 = requests.post(f"{BASE_URL}/message", json=msg3)
    data3 = resp3.json()
    print(f"✓ Stage: {data3['stage']}")
    print(f"✓ Response chars: {len(data3['response'])}\n")

    # 5. Closing (Proposição de consulta) - QUARTA MENSAGEM
    print("5️⃣  CLOSING: Quarta pergunta para trigger solução...")
    msg4 = {"session_token": session, "message": "Isso é possível?"}
    resp4 = requests.post(f"{BASE_URL}/message", json=msg4)
    data4 = resp4.json()
    print(f"✓ Stage: {data4['stage']}")
    print(f"✓ Action: {data4.get('action', 'N/A')}")
    if "closing" in data4['stage']:
        print(f"✓ ✅ APRESENTOU SOLUÇÃO/CLOSING!\n")

    # 6. Contato (Coleta de dados)
    print("6️⃣  CONTACT: Enviando dados do cliente...")
    contact_data = {
        "session_token": session,
        "client_name": "João Silva",
        "client_email": "joao@example.com",
        "client_phone": "+5511987654321",
        "preferencia_consulta": "online"
    }
    resp5 = requests.post(f"{BASE_URL}/contact", json=contact_data)

    if resp5.status_code == 200:
        data5 = resp5.json()
        print(f"✓ Status: SUCCESS")
        print(f"✓ Client: {data5.get('client_name', 'N/A')}")
        print(f"✓ Request ID: {data5.get('request_id', 'N/A')}")
        print(f"✓ WhatsApp Message:\n   {data5.get('whatsapp_message', 'N/A')}\n")
        print("=" * 70)
        print("✅ FLUXO COMPLETO FUNCIONANDO!\n")
        return True
    else:
        print(f"❌ Erro: {resp5.status_code}")
        print(f"   {resp5.text}\n")
        return False

if __name__ == "__main__":
    try:
        success = test_agent_flow()
        if not success:
            print("⚠️  Fluxo incompleto - verificar logs do backend")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
