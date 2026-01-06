#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI-specific styles and color management"""

from nicegui.elements.label import Label
from typing import Dict


# Color palette
COLORS = {
    'green': '#CDFFD2',
    'red': '#FFD2CD',
    'blue': '#CDD2FF',
    'grey': '#9E9E9E',
}

# Global label registry for updating styles
labels: Dict[str, Label] = {}


def default_style(bg: str = '#E8F5E9') -> str:
    """Get default label style with specified background color.
    
    Args:
        bg: Background color hex code
        
    Returns:
        CSS style string
    """
    return (
        f'font-size: 1.5rem; font-weight: 500; padding: 16px; '
        f'background-color: {bg}; width: 100%; text-align: center; color: #000;'
    )


def change_color(target_label: str, new_color: str):
    """Change the color of a registered label.
    
    Args:
        target_label: Name of the label to update
        new_color: Color name ('green', 'red', 'blue', 'grey')
    """
    if target_label in labels:
        color = COLORS.get(new_color, '#9E9E9E')
        label: Label = labels[target_label]
        label.style(default_style(color))
        label.update()


def update_dashboard_colors(dashboard):
    """Update all dashboard label colors based on state.
    
    Args:
        dashboard: DashboardState instance
    """
    change_color("Project", 'green' if dashboard.project_set else 'red')
    change_color("Camera", 'green' if dashboard.camera_set else 'red')
    change_color("Robot", 'green' if dashboard.robot_set else 'red')
    change_color("TMS", 'green' if dashboard.tms_set else 'red')
    change_color("Nasion", 'green' if dashboard.image_NA_set else 'red')
    change_color("Right Fiducial", 'green' if dashboard.image_RE_set else 'red')
    change_color("Left Fiducial", 'green' if dashboard.image_LE_set else 'red')
    change_color("Nose", 'green' if dashboard.tracker_NA_set else 'red')
    change_color("Right Tragus", 'green' if dashboard.tracker_RE_set else 'red')
    change_color("Left Tragus", 'green' if dashboard.tracker_LE_set else 'red')
    change_color("Target", 'green' if dashboard.target_set else 'red')
    change_color("Moving", 'green' if dashboard.robot_moving else 'red')
    change_color("Coil", 'green' if dashboard.at_target else 'red')
    change_color("Trials", 'green' if dashboard.trials_started else 'red')
