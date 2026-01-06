#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TMS Dashboard - Auto-detect and launch available framework"""

import sys


def main():
    """Main entry point with automatic framework detection.
    
    Tries to launch NiceGUI first, then falls back to Streamlit.
    If neither framework is available, prints installation instructions.
    """
    # Try NiceGUI first
    try:
        from src.tms_dashboard.nicegui_app.main import main as nicegui_main
        print("🚀 Iniciando TMS Dashboard com NiceGUI...")
        print("📡 Acesse: http://localhost:8084")
        nicegui_main()
        return
    except ImportError as e:
        print(f"⚠️  NiceGUI não disponível: {e}")
    
    # Fallback to Streamlit
    try:
        import subprocess
        import os
        
        streamlit_main_path = os.path.join(
            "src", "tms_dashboard", "streamlit_app", "main.py"
        )
        
        if os.path.exists(streamlit_main_path):
            print("🚀 Iniciando TMS Dashboard com Streamlit...")
            print("💡 Use Ctrl+C para parar o servidor")
            subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_main_path])
            return
        else:
            raise ImportError("Streamlit main.py not found")
            
    except (ImportError, FileNotFoundError) as e:
        print(f"⚠️  Streamlit não disponível: {e}")
    
    # No framework available
    print("\n" + "=" * 60)
    print("❌ Nenhum framework disponível!")
    print("=" * 60)
    print("\n📦 Instale um dos frameworks:")
    print("\n  Para NiceGUI:")
    print("    uv sync --extra nicegui")
    print("      ou")
    print("    uv add nicegui")
    print("\n  Para Streamlit:")
    print("    uv sync --extra streamlit")
    print("      ou")
    print("    uv add streamlit")
    print("\n  Para ambos:")
    print("    uv sync --extra all")
    print("=" * 60)
    sys.exit(1)


if __name__ == "__main__":
    main()
