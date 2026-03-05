import sys
sys.path.insert(0, '.')

try:
    print("Step 1: Import FastAPI...")
    from fastapi import FastAPI
    print("  OK")

    print("Step 2: Import CORS...")
    from fastapi.middleware.cors import CORSMiddleware
    print("  OK")

    print("Step 3: Import main app...")
