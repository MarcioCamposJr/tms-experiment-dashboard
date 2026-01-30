#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Navigation controls widget."""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState


def create_navigation_controls(dashboard: DashboardState):
    """Create navigation and robot control buttons.
    
    Contains two columns:
    - Navigation Controls: START NAVIGATION, Create Target
    - Robot Control: Free Drive, Active Robot, Move Upward
    
    Args:
        dashboard: DashboardState instance
    """
    # Navigation Controls column
    with ui.column().style('gap: 10px; flex: 1; height: 100%;'):
        with ui.column().classes('w-full').style('gap: 10px; flex: 1;'):
            ui.label('Navigation Controls').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
            
            # Main control button - Start/Stop (highlighted)
            nav_button = ui.button('NAVIGATION STATUS', icon='play_arrow').props('color=positive size=lg').classes('w-full').style(
                'font-size: 1rem; '
                'font-weight: 600; '
                'padding: 16px; '
                'min-height: 60px;'
            )
            # Save UI reference so the updater can change its color
            try:
                dashboard.navigation_button_ui = nav_button
            except Exception:
                # dashboard may be a simple object without that attribute in some tests
                pass
            
            ui.separator().style('margin: 4px 0;')
            
            # Create Target button
            def _create_target_click(e=None):
                # Import inside handler to avoid circular imports
                try:
                    from tms_dashboard.nicegui_app.run import socket_client
                except Exception as exc:
                    print(f"[UI] Could not import socket_client: {exc}")
                    ui.notify('Error: connection not available', position='top')
                    return

                if not socket_client.is_connected:
                    ui.notify('Relay server not connected', position='top')
                    return

                success = socket_client.send_create_marker()
                if success:
                    ui.notify('Create target sent', position='top')
                else:
                    ui.notify('Failed to send Create marker', position='top')

            ui.button('Create Target', icon='add_location_alt', on_click=_create_target_click).props('outlined color=primary').classes('w-full').style(
                'font-size: 0.95rem; '
                'min-height: 50px;'
            )
    
    # Robot Control column
    with ui.column().style('gap: 5px; flex: 1; height: 100%;'):
        ui.label('Robot Control').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
        
        ui.button('Free Drive Robot', icon='gesture').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )

        ui.separator().style('margin: 4px 0;')
        
        ui.button('Active Robot', icon='settings_remote').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )
        
        ui.separator().style('margin: 4px 0;')

        ui.button('Move Upward Robot', icon='arrow_upward').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )
