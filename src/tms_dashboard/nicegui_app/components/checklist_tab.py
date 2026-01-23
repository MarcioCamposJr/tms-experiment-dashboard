#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checklist tab component for NiceGUI app"""

from nicegui import ui
from ...core.dashboard_state import DashboardState


@ui.refreshable
def create_checklist_tab(dashboard: DashboardState):
    """Create the checklist tab content.
    
    Args:
        dashboard: DashboardState instance
    """
    with ui.column().classes('w-full p-4 gap-4'):
        ui.label('Experiment Checklist').style('font-size: 1.25rem; font-weight: 600;')
        
        # Display checklist items
        for i, item in enumerate(dashboard.experiment_checklist):
            with ui.row().classes('w-full items-center gap-2'):
                ui.checkbox('').bind_value(dashboard.checklist_checked, str(i))
                ui.input(value=item).on_value_change(lambda e, idx=i: update_checklist_item(dashboard, idx, e.value)).classes('flex-grow')
                ui.button(icon='delete', on_click=lambda idx=i: delete_checklist_item(dashboard, idx)).props('flat dense')
        
        ui.button('Add Step', icon='add', on_click=lambda: add_checklist_item(dashboard)).classes('mt-4')


def update_checklist_item(dashboard: DashboardState, idx: int, new_value: str):
    """Update a checklist item."""
    dashboard.experiment_checklist[idx] = new_value
    create_checklist_tab.refresh()


def delete_checklist_item(dashboard: DashboardState, idx: int):
    """Delete a checklist item."""
    del dashboard.experiment_checklist[idx]
    # Reindex the checked dict
    new_checked = {}
    for j in range(len(dashboard.experiment_checklist) + 1):
        key = str(j)
        if key in dashboard.checklist_checked:
            if j < idx:
                new_checked[str(j)] = dashboard.checklist_checked[key]
            elif j > idx:
                new_checked[str(j - 1)] = dashboard.checklist_checked[key]
    dashboard.checklist_checked = new_checked
    create_checklist_tab.refresh()


def add_checklist_item(dashboard: DashboardState):
    """Add a new checklist item."""
    dashboard.experiment_checklist.append('New step')
    dashboard.checklist_checked[str(len(dashboard.experiment_checklist) - 1)] = False
    create_checklist_tab.refresh()