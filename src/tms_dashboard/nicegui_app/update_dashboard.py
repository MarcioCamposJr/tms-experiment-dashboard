#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update dashboard module - manages real-time UI updates."""

import logging

import numpy as np
import plotly.graph_objects as go

from tms_dashboard.nicegui_app.styles import change_color, change_radio_icon, change_label, get_status, change_button, change_icon, change_progress_ui, change_image
from tms_dashboard.config import IMAGES_DIR

logger = logging.getLogger(__name__)

class UpdateDashboard:
    def __init__(self, dashboard, emg_connection, client_manager):
        self.dashboard = dashboard
        self.emg_connection = emg_connection
        self.client_manager = client_manager
        self._time_series_snapshot = None
        self._time_series_data = {}

    def update_single(self, ui_state):
        """Update a single client's UI. Called by per-client ui.timer on event loop."""
        updates = [
            self.update_dashboard_colors,
            self.update_indicators,
            self.update_buttons,
            self.update_displacement_plot,
            self.update_rotation_plot,
        ]
        if self.dashboard.status_new_mep:
            updates.append(self.update_mep_plot)
        for update in updates:
            section = update.__name__
            try:
                update(ui_state)
            except Exception as error:
                # Log a persistent failure once, without stopping the other panels.
                signature = (type(error), str(error))
                if ui_state.update_errors.get(section) != signature:
                    logger.exception('UI update failed: client=%s section=%s', ui_state.client_id, section)
                ui_state.update_errors[section] = signature
            else:
                ui_state.update_errors.pop(section, None)

    def update(self):
        """Update all clients (legacy — kept for compatibility)."""
        ui_states = self.client_manager.get_all_clients()
        for ui_state in ui_states:
            try:
                self.update_single(ui_state)
            except Exception as e:
                print(f"Error updating client: {e}")

    def update_dashboard_colors(self, ui_state):
        """Update all dashboard label colors based on state.
        
        Args:
            ui_state: DashboardUI instance
        """
        dashboard = self.dashboard
        
        change_color(ui_state, "camera", get_status(dashboard.camera_set))
        change_color(ui_state, "robot", get_status(dashboard.robot_set))
        change_color(ui_state, "emg", get_status(self.emg_connection.get_connection()))

        if dashboard.probe_visible:
            path_probe = str(IMAGES_DIR / 'visibilities_markers_icon/stylus_icon_green.png') 
        else:
            path_probe = str(IMAGES_DIR / 'visibilities_markers_icon/stylus_icon.png')
        change_image(ui_state, "probe", path_probe)

        if dashboard.head_visible:
            path_head = str(IMAGES_DIR / 'visibilities_markers_icon/head_icon_green.png') 
        else:
            path_head = str(IMAGES_DIR / 'visibilities_markers_icon/head_icon.png')
        change_image(ui_state, "head", path_head)

        if dashboard.coil_visible:
            path_coil = str(IMAGES_DIR / 'visibilities_markers_icon/coil_no_handle_icon_green.png') 
        else:
            path_coil = str(IMAGES_DIR / 'visibilities_markers_icon/coil_no_handle_icon.png')
        change_image(ui_state, "coil", path_coil)

        status = get_status(dashboard.image_fiducials)
        change_color(ui_state, "image_fiducials", status)
        change_radio_icon(ui_state, "image_fiducials", status)

        status = get_status(dashboard.tracker_fiducials)
        change_color(ui_state, "tracker_fiducials", status)
        change_radio_icon(ui_state, "tracker_fiducials", status)

        change_color(ui_state, "target", get_status(dashboard.target_set))
        change_color(ui_state, "moving", get_status(dashboard.robot_moving))
        change_color(ui_state, "coil", get_status(dashboard.at_target))

    def update_indicators(self, ui_state):
        """Update all dashboard indicators."""
        dashboard = self.dashboard
        change_label(ui_state, "distance", str(round(dashboard.module_displacement, 2)) + " mm")
        change_progress_ui(ui_state, "force_indicator", round(dashboard.force, 2))

    def update_displacement_plot(self, ui_state):
        """Apply the latest shared displacement snapshot to this client's plot."""
        self._update_time_series_plot(ui_state, 'displacement')

    def update_rotation_plot(self, ui_state):
        """Apply the latest shared rotation snapshot to this client's plot."""
        self._update_time_series_plot(ui_state, 'rotation')

    def _update_time_series_plot(self, ui_state, kind):
        plot = getattr(ui_state, f'{kind}_plot')
        if plot is None:
            return
        snapshot = self.dashboard.get_time_series_snapshot()
        revision_key = f'last_{kind}_revision'
        if getattr(ui_state, revision_key) == snapshot.revision:
            return

        if self._time_series_snapshot is not snapshot:
            self._time_series_data = {
                name: (
                    getattr(snapshot, f'{name}_time'),
                    getattr(snapshot, name),
                    self._trigger_shapes(getattr(snapshot, f'{name}_time'), snapshot.trigger_times),
                )
                for name in ('displacement', 'rotation')
            }
            self._time_series_snapshot = snapshot

        time_data, series, shapes = self._time_series_data[kind]
        for trace, values in zip(plot.figure.data, series):
            trace.x = time_data
            trace.y = values
        plot.figure.layout.shapes = shapes
        plot.figure.layout.xaxis.autorange = True
        plot.update()
        # A failed send must leave this revision pending for a later retry.
        setattr(ui_state, revision_key, snapshot.revision)

    @staticmethod
    def _trigger_shapes(time_data, trigger_times):
        """Build all stimulus markers together to avoid repeated Plotly validation."""
        visible_times = set(time_data)
        return [
            dict(
                type='line', x0=trigger, x1=trigger, xref='x',
                y0=0, y1=1, yref='y domain',
                line=dict(color='red', width=2, dash='dash'), opacity=0.8,
            )
            for trigger in trigger_times
            if trigger in visible_times
        ]
    
    def update_mep_plot(self, ui_state, num_windows=5):
        """Update MEP plot with current history data using Plotly."""
        
        dashboard = self.dashboard
        if ui_state.mep_plot is None:
            return
            
        # Fetch data
        t_min_ms = self.emg_connection.t_min * 1000
        t_max_ms = self.emg_connection.t_max * 1000
        
        # No action when no data available
        if not dashboard.mep_history_baseline:
            return
            
        mep_history = list(dashboard.mep_history_baseline)[-num_windows:]
        mep_p2p_history = list(dashboard.mep_p2p_history_baseline)[-num_windows:]

        # X Axis
        t_ms = np.linspace(t_min_ms, t_max_ms, len(mep_history[0]))
        
        traces = []
        
        # History (gray lines)
        for i, mep in enumerate(mep_history[:-1]):
            traces.append(go.Scatter(
                x=t_ms, y=mep,
                mode='lines',
                line=dict(color='rgba(128, 128, 128, 0.5)', width=1.5),
                showlegend=False,
                hoverinfo='skip', # Optimization: ignores hover on history 
                name=f'Trial {i}'
            ))
            # Annotation for history (optional, keeps it cleaner if only on last? User asked for "on the curve")
            if i < len(mep_p2p_history):
                peak_idx = np.argmax(mep)
                traces.append(go.Scatter(
                    x=[t_ms[peak_idx]], y=[mep[peak_idx]],
                    mode='text',
                    text=[f'{mep_p2p_history[i]:.0f} uV'],
                    textposition='top center',
                    textfont=dict(color='gray', size=18),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
        # Last MEP (highlighted in red color)
        if len(mep_history) > 0:
            last_mep = mep_history[-1]
            traces.append(go.Scatter(
                x=t_ms, y=last_mep,
                mode='lines',
                line=dict(color='#dc2626', width=3),
                name='Last Response',
                showlegend=False 
            ))
            if len(mep_p2p_history) > 0:
                peak_idx = np.argmax(last_mep)
                traces.append(go.Scatter(
                    x=[t_ms[peak_idx]], y=[last_mep[peak_idx]],
                    mode='text',
                    text=[f'{mep_p2p_history[-1]:.0f} µV'],
                    textposition='top center',
                    textfont=dict(color='#dc2626', size=24, weight='bold'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
        # Updates figure
        # Updating whole chart to avoid Plotly's validation errors
        # "The data property of a figure may only be assigned..."
        # Keeping original layout
        ui_state.mep_plot.figure = go.Figure(data=traces, layout=ui_state.mep_plot.figure.layout)
        # Forces update
        ui_state.mep_plot.update()

        self.dashboard.status_new_mep = False

    def update_buttons(self, ui_state):
        dashboard = self.dashboard
        """Update all dashboard buttons."""
        change_button(ui_state, "navigation_button", get_status(dashboard.navigation_button_pressed))
        change_button(ui_state, "upward_robot_button", get_status(dashboard.move_upward_robot_pressed), ("#5898d46c", "#ffffff00"))
        change_button(ui_state, "active_robot_button", get_status(dashboard.active_robot_pressed), ("#5898d46c", "#ffffff00"))  
        change_button(ui_state, "free_drive_button", get_status(dashboard.free_drive_robot_pressed), ("#5898d46c", "#ffffff00"))
