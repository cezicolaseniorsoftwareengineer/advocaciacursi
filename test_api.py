import time
import requests

time.sleep(2)

# Test health
try:
    r = requests.get('http://localhost:8000/api/v1/health', timeout=5)
    print("✅ Health:", r.status_code, r.json())
except Exception as e:
    print("❌ Health Error:", e)

# Test init
try:
    r = requests.post('http://localhost:8000/api/v1/chat/init', timeout=5)
    print("✅ Init:", r.status_code)
    data = r.json()
    print("   Token:", data.get('session_token')[:20], "...")
    print("   Message:", data.get('message')[:60], "...")
except Exception as e:
    print("❌ Init Error:", e)

# Test message
try:
    r = requests.post('http://localhost:8000/api/v1/chat/init', timeout=5)
    token = r.json()['session_token']
    r2 = requests.post('http://localhost:8000/api/v1/chat/message', json={
        "session_token": token,
        "message": "Preciso de ajuda com direito trabalhista"
    }, timeout=5)
    print("✅ Message:", r2.status_code)
    data = r2.json()
    print("   Response:", data.get('response')[:60], "...")
except Exception as e:
    print("❌ Message Error:", e)
