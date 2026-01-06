#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard tabs component - Improved Status Layout"""

from nicegui import ui
from ...core.dashboard_state import DashboardState
from ..styles import labels, status_badge_style, modern_card_style, section_title_style


def create_dashboard_tabs(dashboard: DashboardState):
    """Create dashboard with improved horizontal status indicators.
    
    Args:
        dashboard: DashboardState instance
    """
    # Main container
    with ui.column().classes('w-full gap-4').style('padding: 20px; background-color: #f9fafb; min-height: calc(100vh - 73px);'):
        
        # === CONNECTION STATUS - Horizontal List ===
        with ui.card().classes('w-full').style(modern_card_style() + 'padding: 20px;'):
            ui.label('Connection Status').style(section_title_style() + 'margin-bottom: 12px;')
            
            with ui.row().classes('w-full gap-8 items-center justify-around'):
                # Project
                with ui.row().classes('items-center gap-3'):
                    ui.icon('folder', size='2rem').style('color: #6b7280;')
                    with ui.column().classes('gap-1'):
                        ui.label('Project').style('font-size: 0.75rem; color: #9ca3af; font-weight: 500; text-transform: uppercase;')
                        label = ui.label('Disconnected').style(status_badge_style('neutral') + 'font-size: 0.875rem;')
                        labels['Project'] = label
                
                # Robot
                with ui.row().classes('items-center gap-3'):
                    ui.icon('precision_manufacturing', size='2rem').style('color: #6b7280;')
                    with ui.column().classes('gap-1'):
                        ui.label('Robot').style('font-size: 0.75rem; color: #9ca3af; font-weight: 500; text-transform: uppercase;')
                        label = ui.label('Disconnected').style(status_badge_style('neutral') + 'font-size: 0.875rem;')
                        labels['Robot'] = label
                
                # Camera
                with ui.row().classes('items-center gap-3'):
                    ui.icon('videocam', size='2rem').style('color: #6b7280;')
                    with ui.column().classes('gap-1'):
                        ui.label('Camera').style('font-size: 0.75rem; color: #9ca3af; font-weight: 500; text-transform: uppercase;')
                        label = ui.label('Disconnected').style(status_badge_style('neutral') + 'font-size: 0.875rem;')
                        labels['Camera'] = label
                
                # TMS
                with ui.row().classes('items-center gap-3'):
                    ui.icon('flash_on', size='2rem').style('color: #6b7280;')
                    with ui.column().classes('gap-1'):
                        ui.label('TMS').style('font-size: 0.75rem; color: #9ca3af; font-weight: 500; text-transform: uppercase;')
                        label = ui.label('Disconnected').style(status_badge_style('neutral') + 'font-size: 0.875rem;')
                        labels['TMS'] = label
        
        # === TWO COLUMN LAYOUT ===
        with ui.row().classes('w-full gap-4'):
            
            # LEFT: FIDUCIALS
            with ui.column().classes('flex-1'):
                with ui.card().classes('w-full').style(modern_card_style() + 'padding: 18px;'):
                    ui.label('Fiducial Registration').style(section_title_style() + 'margin-bottom: 10px;')
                    
                    # Image Fiducials - Horizontal
                    ui.label('Image Fiducials').style('font-size: 0.8125rem; color: #6b7280; font-weight: 600; margin-bottom: 8px;')
                    with ui.row().classes('w-full gap-4 mb-4'):
                        for fid_name, icon_name in [('Left', 'Left Fiducial'), ('Nasion', 'Nasion'), ('Right', 'Right Fiducial')]:
                            with ui.row().classes('items-center gap-2 flex-1'):
                                ui.icon('location_on', size='1.25rem').style('color: #6b7280;')
                                with ui.column().classes('gap-0'):
                                    ui.label(fid_name).style('font-size: 0.6875rem; color: #9ca3af;')
                                    label = ui.label('Off').style(status_badge_style('neutral') + 'font-size: 0.75rem; padding: 3px 8px;')
                                    labels[icon_name] = label
                    
                    ui.separator().style('margin: 10px 0;')
                    
                    # Tracker - Horizontal
                    ui.label('Tracker Landmarks').style('font-size: 0.8125rem; color: #6b7280; font-weight: 600; margin-bottom: 8px;')
                    with ui.row().classes('w-full gap-4'):
                        for trac_name, label_name in [('L Tragus', 'Left Tragus'), ('Nose', 'Nose'), ('R Tragus', 'Right Tragus')]:
                            with ui.row().classes('items-center gap-2 flex-1'):
                                ui.icon('my_location', size='1.25rem').style('color: #6b7280;')
                                with ui.column().classes('gap-0'):
                                    ui.label(trac_name).style('font-size: 0.6875rem; color: #9ca3af;')
                                    label = ui.label('Off').style(status_badge_style('neutral') + 'font-size: 0.75rem; padding: 3px 8px;')
                                    labels[label_name] = label
            
            # RIGHT: ROBOT CONTROL
            with ui.column().classes('flex-1'):
                with ui.card().classes('w-full').style(modern_card_style() + 'padding: 18px;'):
                    ui.label('Robot Control').style(section_title_style() + 'margin-bottom: 10px;')
                    
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        for ctrl_label, icon_name, label_key in [
                            ('Target', 'gps_fixed', 'Target'),
                            ('Coil', 'cable', 'Coil'),
                            ('Moving', 'sync', 'Moving'),
                            ('Trials', 'science', 'Trials')
                        ]:
                            with ui.row().classes('items-center gap-3'):
                                ui.icon(icon_name, size='1.75rem').style('color: #6b7280;')
                                with ui.column().classes('gap-1'):
                                    ui.label(ctrl_label).style('font-size: 0.75rem; color: #9ca3af; font-weight: 500;')
                                    label = ui.label('Inactive').style(status_badge_style('neutral'))
                                    labels[label_key] = label
