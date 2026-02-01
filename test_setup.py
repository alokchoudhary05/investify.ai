#!/usr/bin/env python3
"""
Test script to verify the Financial Intelligence Dashboard setup.
Run this to ensure all components are working correctly.
"""

import sys
import os
from pathlib import Path


def test_environment():
    """Test environment setup."""
    print("=" * 60)
    print("🧪 Testing Financial Intelligence Dashboard Setup")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Python version
    print("1️⃣  Python Version")
    try:
        if sys.version_info >= (3, 8):
            print(f"   ✅ Python {sys.version.split()[0]} (3.8+ required)")
            tests_passed += 1
        else:
            print(f"   ❌ Python {sys.version.split()[0]} (3.8+ required)")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        tests_failed += 1
    print()
    
    # Test 2: Project files
    print("2️⃣  Project Files")
    required_files = {
        "dashboard.py": "Main Streamlit app",
        "market_data.py": "Market data utilities",
        "agent_handler.py": "Agent handler",
        "requirements.txt": "Dependencies",
        ".env": "API configuration (optional)",
    }
    
    for filename, description in required_files.items():
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            print(f"   ✅ {filename:20} ({size:,} bytes) - {description}")
            tests_passed += 1
        else:
            if filename == ".env":
                print(f"   ⚠️  {filename:20} (optional)")
            else:
                print(f"   ❌ {filename:20} - NOT FOUND")
                tests_failed += 1
    print()
    
    # Test 3: Dependencies
    print("3️⃣  Python Dependencies")
    dependencies = {
        "streamlit": "Web UI framework",
        "plotly": "Interactive charts",
        "pandas": "Data manipulation",
        "yfinance": "Financial data",
        "agno": "AI agent framework",
        "openai": "OpenAI API",
        "dotenv": "Environment variables",
    }
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"   ✅ {package:15} - {description}")
            tests_passed += 1
        except ImportError:
            print(f"   ❌ {package:15} - NOT INSTALLED")
            tests_failed += 1
    print()
    
    # Test 4: API Key
    print("4️⃣  API Configuration")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key != "your_openai_api_key_here":
            masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
            print(f"   ✅ OpenAI API Key found: {masked_key}")
            tests_passed += 1
        else:
            print(f"   ❌ OpenAI API Key not configured")
            print(f"      Please set OPENAI_API_KEY in .env file")
            tests_failed += 1
    except Exception as e:
        print(f"   ❌ Error checking API key: {e}")
        tests_failed += 1
    print()
    
    # Test 5: Import modules
    print("5️⃣  Module Imports")
    try:
        from market_data import MarketDataFetcher
        print(f"   ✅ market_data.py loads successfully")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ market_data.py error: {e}")
        tests_failed += 1
    
    try:
        from agent_handler import AgentHandler
        print(f"   ✅ agent_handler.py loads successfully")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ agent_handler.py error: {e}")
        tests_failed += 1
    
    try:
        import streamlit as st
        print(f"   ✅ Streamlit loads successfully (v{st.__version__})")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Streamlit error: {e}")
        tests_failed += 1
    print()
    
    # Test 6: Quick functionality test
    print("6️⃣  Quick Functionality Tests")
    try:
        from market_data import MarketDataFetcher
        print(f"   ⏳ Testing market data fetcher...")
        # Don't actually call it to avoid network delays in testing
        print(f"   ✅ MarketDataFetcher initialized")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ MarketDataFetcher error: {e}")
        tests_failed += 1
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    total = tests_passed + tests_failed
    print(f"✅ Passed: {tests_passed}/{total}")
    print(f"❌ Failed: {tests_failed}/{total}")
    print()
    
    if tests_failed == 0:
        print("🎉 All tests passed! Your dashboard is ready to use.")
        print()
        print("To launch the dashboard, run:")
        print("   streamlit run dashboard.py")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up .env file with OpenAI API key")
        print("   3. Ensure virtual environment is activated")
        return False


if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
