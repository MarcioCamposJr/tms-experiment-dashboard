#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Socket.IO client for communication with relay server"""

import time
import socketio
from threading import Lock


class SocketClient:
    """Socket.IO client to communicate with the TMS relay server.
    
    Manages connection to the relay server and buffers incoming messages
    in a thread-safe manner.
    """
    
    def __init__(self, remote_host: str):
        """Initialize socket client.
        
        Args:
            remote_host: URL of the relay server (e.g., 'http://127.0.0.1:5000')
        """
        self.__buffer = []
        self.__remote_host = remote_host
        self.__connected = False
        self.__sio = socketio.Client(reconnection_delay_max=5)
        
        # Register callbacks
        self.__sio.on('connect', self.__on_connect)
        self.__sio.on('disconnect', self.__on_disconnect)
        self.__sio.on('to_robot', self.__on_message_receive)
        
        self.__lock = Lock()
    
    def __on_connect(self):
        """Callback when connection is established."""
        print(f"Connected to {self.__remote_host}")
        self.__connected = True
    
    def __on_disconnect(self):
        """Callback when connection is lost."""
        print("Disconnected")
        self.__connected = False
    
    def __on_message_receive(self, msg):
        """Callback when message is received from server.
        
        Args:
            msg: Message data from server
        """
        self.__lock.acquire(timeout=1)
        self.__buffer.append(msg)
        self.__lock.release()
    
    def get_buffer(self) -> list:
        """Get and clear the message buffer in a thread-safe manner.
        
        Returns:
            List of messages received since last call
        """
        self.__lock.acquire(timeout=1)
        res = self.__buffer.copy()
        self.__buffer = []
        self.__lock.release()
        return res
    
    def connect(self):
        """Connect to the relay server and wait for connection."""
        self.__sio.connect(self.__remote_host, wait_timeout=1)
        
        while not self.__connected:
            print("Connecting...")
            time.sleep(1.0)
    
    @property
    def is_connected(self) -> bool:
        """Check if currently connected to server."""
        return self.__connected
