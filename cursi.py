#!/usr/bin/env python3
"""
🚀 CURSI - Inicializador Completo do Dr. Estevão
Inicia backend, frontend e abre automaticamente no navegador
"""

import subprocess
import time
import webbrowser
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent


def print_header():
    print("\n" + "=" * 60)
    print("  DR. ESTEVAO - ADVOCACIA CURSI")
    print("  Sistema Juridico Multidisciplinar")
    print("=" * 60 + "\n")


def ensure_project_root():
    """Garante execucao a partir da raiz do projeto, independente de onde o script foi chamado."""
    os.chdir(PROJECT_ROOT)
    print(f"   Diretorio de trabalho: {PROJECT_ROOT}")


def start_backend():
    """Inicia o servidor FastAPI em background com logs visiveis."""
    print("   Iniciando Backend (FastAPI)...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.app.main:app",
             "--reload", "--port", "8000", "--log-level", "info"],
            cwd=str(PROJECT_ROOT),
        )
        print("   Backend iniciado na porta 8000")
        return backend_process
    except Exception as e:
        print(f"   ERRO ao iniciar backend: {e}")
        return None


def start_frontend():
    """Inicia servidor HTTP estatico para o frontend."""
    print("   Iniciando Frontend (HTTP Server)...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "5500", "--directory", str(PROJECT_ROOT)],
        cwd=str(PROJECT_ROOT),
    )
    print("   Frontend iniciado na porta 5500")
    return frontend_process

def verify_backend():
    """Verifica se o backend esta respondendo."""
    import urllib.request
    import json

    max_attempts = 15
    for i in range(max_attempts):
        try:
            req = urllib.request.Request(
                'http://localhost:8000/api/v1/chat/init',
                data=b'{}',
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                data = json.loads(response.read())
                if 'session_token' in data:
                    print("   Backend respondendo corretamente")
                    return True
        except Exception:
            if i < max_attempts - 1:
                print(f"   Aguardando backend... ({i+1}/{max_attempts})")
                time.sleep(2)
            else:
                print("   Backend nao respondeu apos aguardar")
                return False

    return False

def open_browser():
    """Abre o navegador na URL correta."""
    print("   Abrindo navegador...")
    time.sleep(1)

    url = "http://localhost:5500"
    try:
        webbrowser.open(url)
        print(f"   Navegador aberto em: {url}")
    except Exception as e:
        print(f"   Nao foi possivel abrir navegador: {e}")
        print(f"   Acesse manualmente: {url}")

def show_status():
    """Exibe status do sistema."""
    print("\n" + "=" * 60)
    print("  SISTEMA COMPLETO - OPERACIONAL")
    print("=" * 60)
    print(f"\n  Frontend:   http://localhost:5500")
    print(f"  Backend:    http://localhost:8000")
    print(f"  Dr. Estevao pronto para atendimento.\n")
    print("  Pressione CTRL+C para encerrar\n")
    print("=" * 60 + "\n")

def main():
    print_header()
    ensure_project_root()

    backend_process = None
    frontend_process = None

    try:
        # 1. Inicia Backend
        backend_process = start_backend()
        if not backend_process:
            print("   Falha ao iniciar backend. Abortando.")
            sys.exit(1)

        # 2. Verifica Backend
        if not verify_backend():
            print("   Backend nao esta respondendo. Verifique os logs acima.")
            sys.exit(1)

        # 3. Inicia Frontend
        frontend_process = start_frontend()
        time.sleep(1)

        # 4. Abre navegador
        open_browser()

        # 5. Exibe status
        show_status()

        # 6. Mantem rodando
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n   Encerrando sistema...")

        if backend_process:
            backend_process.terminate()
            print("   Backend encerrado")

        if frontend_process:
            frontend_process.terminate()
            print("   Frontend encerrado")

        print("   Sistema parado.\n")
        sys.exit(0)

    except Exception as e:
        print(f"\n   Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
