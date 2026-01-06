#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI web application main entry point"""

import threading
import queue
import time
from nicegui import ui

from ..config import DEFAULT_HOST, DEFAULT_PORT, NICEGUI_PORT
from ..core.dashboard_state import DashboardState
from ..core.socket_client import SocketClient
from ..core.message_handler import MessageHandler
from .styles import update_dashboard_colors
from .components import (
    create_header,
    create_experiment_form,
    create_dashboard_tabs
)


def main():
    """Main entry point for NiceGUI application."""
    
    # Initialize core components
    dashboard = DashboardState()
    socket_client = SocketClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
    message_handler = MessageHandler(socket_client, dashboard)
    
    # Connect to relay server
    socket_client.connect()
    print("Conectado à rede local")
    
    # Queue for threading communication
    message_queue = queue.Queue()
    
    # Background thread for message processing
    def process_messages_loop():
        """Continuously process messages and update dashboard."""
        while True:
            time.sleep(0.5)
            message = message_handler.process_messages()
            message_queue.put(message)
            update_dashboard_colors(dashboard)
    
    # Start message processing thread
    threading.Thread(target=process_messages_loop, daemon=True).start()
    
    # Build UI
    create_header()
    create_experiment_form(dashboard)
    create_dashboard_tabs(dashboard)
    
    # Run NiceGUI server
    ui.run(port=NICEGUI_PORT, reload=False)


if __name__ == "__main__":
    main()
