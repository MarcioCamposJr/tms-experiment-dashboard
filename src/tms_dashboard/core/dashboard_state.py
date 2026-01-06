#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard state management - framework agnostic"""

from dataclasses import dataclass
import numpy as np


@dataclass
class DashboardState:
    """Central state object for the TMS experiment dashboard.
    
    This class holds all state information including:
    - Connection status (project, camera, robot, TMS)
    - Image and tracker fiducials
    - Navigation data (locations, displacements)
    - Experiment metadata
    """
    
    def __init__(self):
        # Connection and setup status
        self.project_set = False
        self.camera_set = False
        self.robot_set = False
        self.tms_set = False
        
        # Image fiducials (set in software)
        self.image_NA_set = False  # Nasion
        self.image_RE_set = False  # Right ear
        self.image_LE_set = False  # Left ear
        
        # Tracker fiducials (real world landmarks)
        self.tracker_NA_set = False  # Nose
        self.tracker_RE_set = False  # Right tragus
        self.tracker_LE_set = False  # Left tragus
        
        # Robot and navigation status
        self.matrix_set = False
        self.target_set = False
        self.robot_moving = False
        self.at_target = False
        self.trials_started = False
        
        # Navigation position/orientation data (x, y, z, rx, ry, rz)
        self.displacement = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.probe_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.head_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.coil_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.target_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        
        # Experiment metadata with default values
        self.experiment_name = 'Paired pulse, dual site, bilateral, leftM1-rightPMv'
        self.experiment_description = 'Dual site paired bilateral TMS stimulation, with 2 channel EMG acquisition. 80 trials, 4 experimental conditions, 200 pulses'
        self.start_date = '2025-01-31'
        self.end_date = '2024-02-01'
        self.experiment_details = 'Paired pulse contralateral conditioning. Paradigm with motor mapping totaling 80 trials with 20 pulses/condition. Target muscle: APB. Inter-pulse interval: 7 to 10 s.'
        
        # Stimulation parameters
        self.conditioning_stimulus = 'right ventral premotor cortex (rPMv)'
        self.test_stimulus = 'left M1'
        self.number_intervals = '30'
        self.interval_step = '15'  # ms
        self.number_trials = '120'
        self.number_conditions = '4'
        self.trials_per_condition = '30'
        self.intertrial_interval = '12'  # ms
