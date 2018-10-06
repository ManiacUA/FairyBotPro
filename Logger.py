"""How to write logs for FairyBotPro.
What should be logged:
1) Start at the start of a function.
2) Finish at the end of function.
3) Result of any action/request.

Rules:
1) Logs initialisation should be first step of initialisation of module;
2) Entities should never be monitored;
3) Modules should have add_tabs=1, functions should increase their tabs when called one inside another
"""

import Tool
import datetime


class Logger:
    func = "(func not set)"
    tab = "  "  # for saving space purpose tab is 2 spaces

    def __init__(self, module, account, add_tabs=0, show_logs=True, show_warnings=True):
        self.add_tabs = add_tabs
        self.module = module
        self.show_logs = show_logs
        self.show_warnings = show_warnings
        self.log(account, "Logger initialised in this module.")

    def set_func(self, func):
        """Sets func in message to this value. Custom parameter in message will use custom but won't override it."""
        self.func = func

    def log(self, account, text, func=None, tabs=0):
        if self.show_logs:
            Tool.Sprint("... " + self._message(self, account, text, func, tabs))

    def warning(self, account, text, func=None, tabs=0):
        if self.show_warnings:
            Tool.Sprint("!!! " + self._message(self, account, text, func, tabs))

    def error(self, account, text, func=None, tabs=0):
        Tool.Sprint("ERR " + self._message(self, account, text, func, tabs))
        exit()  # TODO: check if that thing will stop thread or whole script or probably just throw exception

    def _message(self, account, text, func, tabs):
        time_string = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        if func is None:
            func = self.func
        text = "{}[{}] {}{}({}): {}".format(
            time_string, account.email, (self.add_tabs + tabs) * self.tab, self.module, func, text)
        return text
