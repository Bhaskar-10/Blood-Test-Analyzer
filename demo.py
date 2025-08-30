#!/usr/bin/env python3
"""
Demo script for Blood Test Analyzer
This script demonstrates the application functionality without needing a real PDF.
"""

import requests
import json
import os
from dotenv import load_dotenv

def test_backend_health():
    """Test if the backend is running"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on http://localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def main():
    """Main demo function"""
    print("🩸 Blood Test Analyzer - Demo")
    print("=" * 40)
    
    # Load environment
    load_dotenv()
    
    # Test backend health
    print("\n1. Testing backend health...")
    if not test_backend_health():
        print("\n❌ Backend is not running!")
        print("Please start the backend first:")
        print("python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("\n🎉 Demo completed!")
    print("\n📋 Next steps:")
    print("1. Start the Streamlit frontend: streamlit run streamlit_app.py")
    print("2. Or use the startup script: python start_app.py")
    print("3. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
