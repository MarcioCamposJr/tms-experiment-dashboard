#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI-specific styles and color management - Modern Clean Design"""

from nicegui.elements.label import Label
from typing import Dict


# Modern Color Palette - Clean and Professional
COLORS = {
    'success': '#10b981',      # Green
    'error': '#ef4444',        # Red
    'warning': '#f59e0b',      # Amber
    'info': '#3b82f6',         # Blue
    'neutral': '#6b7280',      # Gray
    'bg_light': '#f9fafb',     # Very light gray
    'bg_card': '#ffffff',      # White
    'border': '#e5e7eb',       # Light gray border
    'text_primary': '#111827', # Almost black
    'text_secondary': '#6b7280' # Gray
}

# Global label registry for updating styles
labels: Dict[str, Label] = {}


def modern_card_style() -> str:
    """Get modern card container style."""
    return (
        'background-color: #ffffff;'
        'border-radius: 12px;'
        'box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);'
        'padding: 24px;'
        'margin-bottom: 16px;'
    )


def status_badge_style(status: str) -> str:
    """Get modern status badge style.
    
    Args:
        status: 'success', 'error', 'warning', 'info', or 'neutral'
        
    Returns:
        CSS style string for badge
    """
    color_map = {
        'success': ('#10b981', '#d1fae5'),
        'error': ('#ef4444', '#fee2e2'),
        'warning': ('#f59e0b', '#fef3c7'),
        'info': ('#3b82f6', '#dbeafe'),
        'neutral': ('#6b7280', '#f3f4f6')
    }
    
    text_color, bg_color = color_map.get(status, color_map['neutral'])
    
    return (
        f'display: inline-flex;'
        f'align-items: center;'
        f'padding: 6px 12px;'
        f'border-radius: 9999px;'
        f'font-size: 0.875rem;'
        f'font-weight: 500;'
        f'background-color: {bg_color};'
        f'color: {text_color};'
        f'border: 1px solid {text_color}33;'
        f'min-width: 100px;'
        f'justify-content: center;'
    )


def section_title_style() -> str:
    """Get section title style."""
    return (
        'font-size: 1.125rem;'
        'font-weight: 600;'
        'color: #111827;'
        'margin-bottom: 12px;'
        'letter-spacing: -0.025em;'
    )


def change_color(dashboard, target_label: str, new_status: str):
    """Change the color of a label and its associated icon.
    
    Apenas duas cores são usadas:
    - 'success': Verde (#10b981) - Estado ativo/conectado
    - 'neutral': Cinza (#9ca3af) - Estado inativo/desconectado
    
    Args:
        dashboard: DashboardState instance containing label and icon references
        target_label: Name of the label to update (will be converted to lowercase)
        new_status: Status - 'success' or 'neutral'
    """
    # Apenas duas cores possíveis
    color = '#10b981' if new_status == 'success' else '#9ca3af'  # Verde ou Cinza
    
    # Update label if exists in dashboard
    label_key = f'label_{target_label.lower().replace(" ", "_")}'
    if hasattr(dashboard, label_key):
        label = getattr(dashboard, label_key)
        label.style(f'font-size: 1.0rem; color: {color}; font-weight: 500;')
        label.update()
    
    # Update associated icon if exists
    icon_key = f'icon_{target_label.lower().replace(" ", "_")}'
    if hasattr(dashboard, icon_key):
        icon = getattr(dashboard, icon_key)
        icon.style(f'font-size: 22px; color: {color};')
        icon.update()

def change_icon(dashboard, target_label: str, new_status: str):
    """Change the icon of a label based on status."""
    icon_key = f'icon_{target_label.lower().replace(" ", "_")}'
    if hasattr(dashboard, icon_key):
        icon = getattr(dashboard, icon_key)
        icon.name = 'radio_button_unchecked' if new_status == 'neutral' else 'radio_button_checked'
        icon.update()


def update_dashboard_colors(dashboard):
    """Update all dashboard label colors based on state.
    
    Args:
        dashboard: DashboardState instance
    """
    # Determine status based on state
    def get_status(condition: bool) -> str:
        return 'success' if condition else 'neutral'
    
    change_color(dashboard, "project", get_status(dashboard.project_set))
    change_color(dashboard, "camera", get_status(dashboard.camera_set))
    change_color(dashboard, "robot", get_status(dashboard.robot_set))
    change_color(dashboard, "tms", get_status(dashboard.tms_set))
    change_color(dashboard, "probe", get_status(dashboard.probe_visible))
    change_color(dashboard, "head", get_status(dashboard.head_visible))
    change_color(dashboard, "coil", get_status(dashboard.coil_visible))

    change_color(dashboard, "nasion", get_status(dashboard.image_NA_set))
    change_icon(dashboard, "nasion", get_status(dashboard.image_NA_set))
    change_color(dashboard, "r_fid", get_status(dashboard.image_RE_set))
    change_icon(dashboard, "r_fid", get_status(dashboard.image_RE_set))
    change_color(dashboard, "l_fid", get_status(dashboard.image_LE_set))
    change_icon(dashboard, "l_fid", get_status(dashboard.image_LE_set))
    change_color(dashboard, "nose", get_status(dashboard.tracker_NA_set))
    change_icon(dashboard, "nose", get_status(dashboard.tracker_NA_set))
    change_color(dashboard, "l_tragus", get_status(dashboard.tracker_LE_set))
    change_icon(dashboard, "l_tragus", get_status(dashboard.tracker_LE_set))

    change_color(dashboard, "target", get_status(dashboard.target_set))
    change_color(dashboard, "moving", get_status(dashboard.robot_moving))
    change_color(dashboard, "coil", get_status(dashboard.at_target))
    # change_color(dashboard, "trials", get_status(dashboard.trials_started))
