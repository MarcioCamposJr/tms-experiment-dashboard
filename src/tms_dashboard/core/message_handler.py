#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Message handler for processing navigation status updates"""

import numpy as np
from typing import Optional
from .dashboard_state import DashboardState
from .socket_client import SocketClient
from ..utils.constants import robot_messages


class MessageHandler:
    """Processes messages from socket client and updates dashboard state."""
    
    def __init__(self, socket_client: SocketClient, dashboard_state: DashboardState):
        """Initialize message handler.
        
        Args:
            socket_client: SocketClient instance to get messages from
            dashboard_state: DashboardState instance to update
        """
        self.socket_client = socket_client
        self.dashboard = dashboard_state
        self.target_status = None
        self.distance_0 = 0
        self.distance_x = 0
        self.distance_y = 0
        self.distance_z = 0
    
    def process_messages(self) -> Optional[dict]:
        """Process all messages in buffer and update dashboard state.
        
        Returns:
            Last processed message or None if no messages
        """
        buf = self.socket_client.get_buffer()
        
        if len(buf) == 0:
            return None
        
        # Check if any message topic is in robot_messages
        if not any(item in [d['topic'] for d in buf] for item in robot_messages):
            return None
        
        topics = [d['topic'] for d in buf]
        
        for i in range(len(buf)):
            if topics[i] in robot_messages:
                self.target_status = buf[i]["data"]
                self._handle_message(topics[i], self.target_status)
        
        return self.target_status
    
    def _handle_message(self, topic: str, data):
        """Handle individual message based on topic.
        
        Args:
            topic: Message topic string
            data: Message data payload
        """
        match topic:
            case 'Set image fiducial':
                self._handle_image_fiducial(data)
            
            case 'Reset image fiducials':
                self.dashboard.image_NA_set = False
                self.dashboard.image_RE_set = False
                self.dashboard.image_LE_set = False
            
            case 'Project loaded successfully':
                self.dashboard.project_set = True
            
            case 'Close Project':
                self.dashboard.project_set = False
            
            case 'From Neuronavigation: Update tracker poses':
                self._handle_tracker_poses(data)
            
            case 'Neuronavigation to Robot: Update displacement to target':
                self._handle_displacement(data)
            
            case 'Tracker changed':
                self.dashboard.camera_set = False
            
            case 'Tracker fiducials set':
                self.dashboard.tracker_LE_set = True
                self.dashboard.tracker_RE_set = True
                self.dashboard.tracker_NA_set = True
            
            case 'Reset tracker fiducials':
                self.dashboard.tracker_NA_set = False
                self.dashboard.tracker_RE_set = False
                self.dashboard.tracker_LE_set = False
            
            case 'Open navigation menu':
                self.dashboard.robot_set = True
                self.dashboard.matrix_set = True
            
            case 'Neuronavigation to Robot: Set target':
                self._handle_set_target(data)
            
            case 'Unset target':
                self.dashboard.target_set = False
            
            case 'Start navigation':
                self.dashboard.robot_moving = True
            
            case 'Coil at target':
                if data['state'] == True:
                    self.dashboard.at_target = True
                    self.dashboard.robot_moving = False
                else:
                    self.dashboard.at_target = False
            
            case 'Trial triggered':
                print(data)
                print(str(self.dashboard.trials_started))
                self.dashboard.trials_started = True
            
            case 'Stop navigation':
                self.dashboard.robot_moving = False
    
    def _handle_image_fiducial(self, data):
        """Handle image fiducial setting/unsetting."""
        if data == "":
            return
        
        if str(data['position']) == "nan":
            match data['fiducial_name']:
                case 'NA':
                    self.dashboard.image_NA_set = False
                case 'RE':
                    self.dashboard.image_RE_set = False
                case 'LE':
                    self.dashboard.image_LE_set = False
        else:
            match data['fiducial_name']:
                case 'NA':
                    self.dashboard.image_NA_set = True
                case 'RE':
                    self.dashboard.image_RE_set = True
                case 'LE':
                    self.dashboard.image_LE_set = True
    
    def _handle_tracker_poses(self, data):
        """Handle tracker pose updates."""
        poses = data['poses']
        
        # Convert angles to degrees
        self.dashboard.probe_location = (
            poses[0][0], poses[0][1], poses[0][2],
            np.degrees(poses[0][3]), np.degrees(poses[0][4]), np.degrees(poses[0][5])
        )
        self.dashboard.head_location = (
            poses[1][0], poses[1][1], poses[1][2],
            np.degrees(poses[1][3]), np.degrees(poses[1][4]), np.degrees(poses[1][5])
        )
        self.dashboard.coil_location = (
            poses[2][0], poses[2][1], poses[2][2],
            np.degrees(poses[2][3]), np.degrees(poses[2][4]), np.degrees(poses[2][5])
        )
        self.dashboard.target_location = (
            poses[3][0], poses[3][1], poses[3][2],
            np.degrees(poses[3][3]), np.degrees(poses[3][4]), np.degrees(poses[3][5])
        )
        self.dashboard.robot_moving = True
    
    def _handle_displacement(self, data):
        """Handle displacement to target update."""
        self.dashboard.displacement = list(map(lambda x: data['displacement'][x], range(6)))
        self.distance_x = self.dashboard.displacement[0]
        self.distance_y = self.dashboard.displacement[1]
        self.distance_z = self.dashboard.displacement[2]
        self.distance_0 = (self.distance_x + self.distance_y + self.distance_z) / 3
        self.dashboard.robot_moving = True
    
    def _handle_set_target(self, data):
        """Handle target setting."""
        target = data['target']
        self.dashboard.target_location = (target[0][3], target[1][3], target[2][3])
        print(self.dashboard.target_location)
        self.dashboard.target_set = True
