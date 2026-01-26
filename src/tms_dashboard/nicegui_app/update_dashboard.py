import numpy as np

from .styles import change_color, change_icon, change_label, get_status

class UpdateDashboard:
    def __init__(self, dashboard, emg_connection):
        self.dashboard = dashboard
        self.emg_connection = emg_connection

    def update(self):
        self.update_dashboard_colors()
        self.update_indicators()
        self.update_displacement_plot()
        self.update_mep_plot()
        self.update_buttons()

    def update_dashboard_colors(self):
        """Update all dashboard label colors based on state.
        
        Args:
            dashboard: DashboardState instance
        """
        dashboard = self.dashboard
        
        change_color(dashboard, "project", get_status(dashboard.project_set))
        change_color(dashboard, "camera", get_status(dashboard.camera_set))
        change_color(dashboard, "robot", get_status(dashboard.robot_set))
        change_color(dashboard, "tms", get_status(dashboard.tms_set))

        change_color(dashboard, "marker_probe", get_status(dashboard.probe_visible))
        change_color(dashboard, "marker_head", get_status(dashboard.head_visible))
        change_color(dashboard, "marker_coil", get_status(dashboard.coil_visible))

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
        change_color(dashboard, "r_tragus", get_status(dashboard.tracker_RE_set))
        change_icon(dashboard, "r_tragus", get_status(dashboard.tracker_RE_set))

        change_color(dashboard, "target", get_status(dashboard.target_set))
        change_color(dashboard, "moving", get_status(dashboard.robot_moving))
        change_color(dashboard, "coil", get_status(dashboard.at_target))
        # change_color(dashboard, "trials", get_status(dashboard.trials_started))

    def update_indicators(self):
        """Update all dashboard indicators."""
        dashboard = self.dashboard
        change_label(dashboard, "distance", str(round(dashboard.module_displacement, 2)) + " mm")
        change_label(dashboard, "force", dashboard.force)

    def update_displacement_plot(self):
        """Update displacement plot with current history data.
        
        Args:
            dashboard: DashboardState instance
        """

        dashboard = self.dashboard
        
        # Convert deques to lists for plotting
        time_data = list(dashboard.displacement_time_history)
        x_data = list(dashboard.displacement_history_x)
        y_data = list(dashboard.displacement_history_y)
        z_data = list(dashboard.displacement_history_z)
        
        # Clear and redraw the plot
        ax = dashboard.displacement_ax
        if ax is None:
            return
        ax.clear()
        
        # Plot the three lines
        ax.plot(time_data, x_data, color='#ef4444', linewidth=2.5, label='X axis')
        ax.plot(time_data, y_data, color='#10b981', linewidth=2.5, label='Y axis')
        ax.plot(time_data, z_data, color='#3b82f6', linewidth=2.5, label='Z axis')
        
        # Restore styling
        ax.set_xlabel('Time (s)', fontsize=10)
        ax.set_ylabel('Displacement (mm)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_facecolor('#fafafa')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        
        # Update the plot widget
        dashboard.displacement_plot.update()
    
    def update_mep_plot(self):
        """Update MEP plot with current history data.
        
        Args:
            dashboard: DashboardState instance
        """
        mep_history = list(self.emg_connection.get_triggered_window())
        if mep_history == self.dashboard.mep_history:
            return
        
        if len(mep_history) == 0:
            return

        dashboard = self.dashboard
        mep_sampling_rate = dashboard.mep_sampling_rate = self.emg_connection.get_sampling_rate()
        
        dashboard.mep_history = mep_history
        ax = dashboard.mep_ax
        ax.clear()

        t_min, tmax = self.emg_connection.t_min *1000, self.emg_connection.t_max *1000
        # t_ms sempre de -10 a 40 ms, número de pontos baseado nas amostras
        t_ms = np.linspace(t_min, tmax, len(mep_history[0]))

        ax.set_xlabel('Time (ms)', fontsize=10)
        ax.set_ylabel('MEP amplitude (uV)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_facecolor('#fafafa')

        for i, mep in enumerate(mep_history[-5:]):
            ax.plot(t_ms, mep, color='gray', alpha=0.5, linewidth=2.5, label='Trial' if i == 0 else None)
        
        ax.plot(t_ms, np.mean(mep_history[-5:], axis=0), color='#ef4444', linewidth=2.5, label='Mean')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        
        # Update the plot widget
        dashboard.mep_plot.update()

    def update_buttons(self):
        dashboard = self.dashboard
        """Update all dashboard buttons."""
        change_color(dashboard, "navigation_button", get_status(dashboard.navigation_button_pressed), ("#21BA45", "#C10015"))