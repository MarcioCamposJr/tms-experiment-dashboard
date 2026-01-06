#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI web application main entry point - Versão simplificada"""

import threading
import time
from nicegui import ui

from ..config import DEFAULT_HOST, DEFAULT_PORT, NICEGUI_PORT
from ..core.dashboard_state import DashboardState
from ..core.socket_client import SocketClient
from ..core.message_handler import MessageHandler
from .styles import update_dashboard_colors
from .components import create_header, create_dashboard_tabs


def main():
    """Main entry point for NiceGUI application."""
    
    # Initialize core components
    dashboard = DashboardState()
    socket_client = SocketClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    message_handler = MessageHandler(socket_client, dashboard)
    
    # Background thread for message processing
    def process_messages_loop():
        """Continuously process messages and update dashboard."""
        while True:
            try:
                time.sleep(0.5)
                message_handler.process_messages()
                update_dashboard_colors(dashboard)
            except Exception:
                pass
    
    # Start message processing thread
    threading.Thread(target=process_messages_loop, daemon=True, name="MessageProcessor").start()
    
    # Start socket client
    socket_client.connect()
    
    # Build UI
    create_header(dashboard)
    create_dashboard_tabs(dashboard)
    
    # Run NiceGUI server
    ui.run(
        port=NICEGUI_PORT,
        reload=False,
        show=False,
        title="TMS Dashboard",
        favicon="🧠"
    )


if __name__ == "__main__":
    print("🚀 Iniciando TMS Dashboard com NiceGUI...")
    print(f"📡 Acesse: http://localhost:8084")
    main()
