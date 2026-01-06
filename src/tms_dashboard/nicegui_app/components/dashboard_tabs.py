#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard tabs component - simplified version"""

from nicegui import ui
from ...core.dashboard_state import DashboardState
from ..styles import labels, default_style


def create_dashboard_tabs(dashboard: DashboardState):
    """Create dashboard main tabs interface.
    
    Args:
        dashboard: DashboardState instance
        
    Note:
        This is a simplified version. Full implementation with all tabs
        (Connections, Transformation, Control, Navigation, Stimulation)
        can be expanded based on the original main_nicegui.py file.
    """
    with ui.expansion('Dashboard Main Functions', icon='expand_more'):
        with ui.tabs().classes('w-full') as tabs:
            connections_tab = ui.tab('Connections')
            transformation_tab = ui.tab('Transformation')
            control_tab = ui.tab('Control')
            navigation_tab = ui.tab('Navigation')
            stimulation_tab = ui.tab('Stimulation')
        
        with ui.tab_panels(tabs, value=connections_tab).classes('w-full'):
            # Connections tab
            with ui.tab_panel(connections_tab):
                with ui.row().classes('w-full'):
                    with ui.column():
                        label = ui.label('Project').style(default_style('#FFFFFF'))
                        labels['Project'] = label
                    with ui.column():
                        label = ui.label('Robot').style(default_style('#FFFFFF'))
                        labels['Robot'] = label
                    with ui.column():
                        label = ui.label('Camera').style(default_style('#FFFFFF'))
                        labels['Camera'] = label
                    with ui.column():
                        label = ui.label('TMS').style(default_style('#FFFFFF'))
                        labels['TMS'] = label
            
            # Transformation tab
            with ui.tab_panel(transformation_tab):
                ui.label('Image fiducials')
                with ui.row().classes('w-full'):
                    with ui.column():
                        label = ui.label('Left Fiducial').style(default_style('#FFFFFF'))
                        labels['Left Fiducial'] = label
                    with ui.column():
                        label = ui.label('Nasion').style(default_style('#FFFFFF'))
                        labels['Nasion'] = label
                    with ui.column():
                        label = ui.label('Right Fiducial').style(default_style('#FFFFFF'))
                        labels['Right Fiducial'] = label
                
                ui.label('Real world landmarks')
                with ui.row().classes('w-full'):
                    with ui.column():
                        label = ui.label('Left Tragus').style(default_style('#FFFFFF'))
                        labels['Left Tragus'] = label
                    with ui.column():
                        label = ui.label('Nose').style(default_style('#FFFFFF'))
                        labels['Nose'] = label
                    with ui.column():
                        label = ui.label('Right Tragus').style(default_style('#FFFFFF'))
                        labels['Right Tragus'] = label
            
            # Control tab
            with ui.tab_panel(control_tab):
                ui.label('Robot control')
                with ui.row().classes('w-full'):
                    with ui.column():
                        label = ui.label('Target').style(default_style('#FFFFFF'))
                        labels['Target'] = label
                    with ui.column():
                        label = ui.label('Coil').style(default_style('#FFFFFF'))
                        labels['Coil'] = label
                    with ui.column():
                        label = ui.label('Moving').style(default_style('#FFFFFF'))
                        labels['Moving'] = label
                    with ui.column():
                        label = ui.label('Trials').style(default_style('#FFFFFF'))
                        labels['Trials'] = label
            
            # Navigation tab (placeholder)
            with ui.tab_panel(navigation_tab):
                ui.label('Navigation panel - To be implemented')
                ui.markdown('*Full 3D visualization and plots will be added here*')
            
            # Stimulation tab (placeholder)
            with ui.tab_panel(stimulation_tab):
                ui.label('Stimulation setup - To be implemented')
                ui.markdown('*Stimulation parameters form will be added here*')
