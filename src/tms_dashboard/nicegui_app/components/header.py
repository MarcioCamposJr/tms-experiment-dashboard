#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header component for NiceGUI app"""

from nicegui import ui
from ...config import IMAGES_DIR


def create_header():
    """Create application header with logo and title."""
    with ui.row().classes('items-center q-pa-md w-full'):
        ui.image(str(IMAGES_DIR / 'biomag_logo.jpg')).classes('w-12 h-12')
        ui.label('Biomag TMS Dashboard').classes('text-h4')
