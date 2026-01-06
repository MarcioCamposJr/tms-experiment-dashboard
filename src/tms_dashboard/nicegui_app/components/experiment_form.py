#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Experiment form component for NiceGUI app"""

from nicegui import ui
from ...core.dashboard_state import DashboardState
from ...core.data_logger import DataLogger
from ...config import CSV_PATH


def create_experiment_form(dashboard: DashboardState):
    """Create experiment details form.
    
    Args:
        dashboard: DashboardState instance
    """
    logger = DataLogger(CSV_PATH)
    
    with ui.expansion('Experiment details', icon='expand_more'):
        ui.label('Edit the experiment details')
        
        name_input = ui.input('Experiment_name', value=dashboard.experiment_name)
        desc_input = ui.input('Experiment_description', value=dashboard.experiment_description)
        start_input = ui.input('Start_date', value=dashboard.start_date)
        end_input = ui.input('End_date', value=dashboard.end_date)
        details_input = ui.input('Experiment_details', value=dashboard.experiment_details)
        
        def save_data():
            """Save experiment data to CSV."""
            data = DataLogger.create_experiment_dict(
                experiment_name=name_input.value,
                experiment_description=desc_input.value,
                start_date=start_input.value,
                end_date=end_input.value,
                experiment_details=details_input.value
            )
            if logger.save_experiment_data(data):
                ui.notify('Dados gravados com sucesso!')
            else:
                ui.notify('Erro ao gravar dados', type='negative')
        
        ui.button('Save', on_click=save_data)
