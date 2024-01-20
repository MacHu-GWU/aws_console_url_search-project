# -*- coding: utf-8 -*-

import zelfred.api as zf

from .ui_def import UI

ui = UI()


def run_ui():
    """
    Run the AWS console url search UI. This is the entry point of the CLI command.
    """
    zf.debugger.reset()
    zf.debugger.enable()
    ui.run()
